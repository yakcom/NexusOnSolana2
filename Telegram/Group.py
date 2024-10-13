from loguru import logger
import Telegram.Bot
import Telegram.General
import Telegram.Topic
import System.Url
import Config,os


def Post(Topic,Token):
    logger.debug(f'Post {Token["Address"]}')
    Telegram.Topic.Post(Token)
    Telegram.General.Post(Topic,Token)

def CreateHeaderBar(Info):
    return (f'<blockquote>'
            f'<b><a href="https://t.me/c/{Telegram.Bot.Group}/{Info["TopicId"]}/{Info["TopicPostId"]}">{Info["Name"].strip().capitalize()}</a></b>\n'
            f'<i>{Info["Description"].strip()}</i>'
            f'</blockquote>\n')

def CreateTokenBar(Info):
    return (f'<blockquote>'
            f'<a href="https://solscan.io/token/{Info["Address"]}"><b>Metadata</b></a>\n'
            f'<b>┌ Symbol: </b><i>{Info["Symbol"]}</i>\n'
            f'<b>├ Name: </b><i>{Info["Name"]}</i>\n'
            f'<b>├ Supply: </b><i>{Info["Supply"]}</i>\n'
            f'<b>├ Decimals: </b><i>{Info["Decimals"]}</i>\n'
            f'<b>└ Tax: </b><i>{Info["Fee"]}%</i>\n'
            f'<a href="https://solscan.io/token/{Info["Address"]}#metadata"><b>Permissions</b></a>\n'
            f'<b>┌ Mintable: </b><i>{Info["Mintable"]}</i>\n'
            f'<b>├ Freezable: </b><i>{Info["Freezable"]}</i>\n'
            f'<b>└ Mutable: </b><i>{Info["Mutable"]}</i>\n'
            f'<a href="https://solscan.io/token/{Info["Owner"]}"><b>Owner</b></a>\n'
            f'<b>┌ Owner: </b><i><a href="https://solscan.io/token/{Info["Owner"]}">{Info["Owner"][:3]}...{Info["Owner"][-3:]}</a></i>\n'
            f'<b>└ Balance: </b><i>{Info["OwnerBalance"]} SOL</i>\n'
            f'<a href="https://solscan.io/token/{Info["Owner"]}#metadata"><b>Sources</b></a>\n'
            f'<b>┌ Storage: </b><i>{Info["Uri"]}</i>\n'
            f'<b>├ Creator: </b><i><a href="{Info["CreatorUrl"]}">{Info["CreatorName"]}</a></i>\n'
            f'<b>└ Dex: </b><i><a href="https://pump.fun/">Pumpfun</a></i>'
            f'</blockquote>\n')

def CreateNotifyBar(Info):
    Notify=[]
    if Info['Similar']:Notify.append(f'<blockquote><b>🔎  <a href="https://t.me/c/{Telegram.Bot.Group}/{Info["TopicId"]}/{Info["TopicPostId"]}">Developer has a history</a></b></blockquote>')
    if Info['Duplicate']: Notify.append(f'<blockquote><b>⚠️  <a href="https://t.me/c/{Telegram.Bot.Group}/{Config.Get("Telegram","NewTokens")}/{Info["Duplicate"]}">Such token already exists</a></b></blockquote>')
    if Info['Freezable']: Notify.append('<blockquote><b>⛔️  Token sale is not possible</b></blockquote>')
    if Info['Mintable']: Notify.append('<blockquote><b>⚠️  Developer can mint more</b></blockquote>')
    if Info['Mutable']: Notify.append('<blockquote><b>⚠️  Developer can change token</b></blockquote>')
    if Info['OwnerBalance']==0: Notify.append('<blockquote><b>⚠️  Developer has zero balance</b></blockquote>')
    if not Info['Socials']: Notify.append('<blockquote><b>⚠️  Socials not found</b></blockquote>')
    Notify = '\n'.join(Notify)
    if Notify:return f'{Notify}\n'
    else:return ''

def CreateAddressBar(Info):
    return f'<pre>{Info["Address"]}</pre>\n\n'

def CreateTagsBar(Info):
    return f'<b>{Info["Tags"]}</b>'

def CreateComparisonBar(Info):
    Similar = Info['Similar']
    if Similar:
        return (f'<blockquote>'
                f'<b><a href="https://t.me/c/{Telegram.Bot.Group}/{Info["TopicId"]}/{Info["TopicLastPostId"]}">Comparison</a></b>\n'
                f'<b>┌ General: </b><i>{Similar["Percent"]}%</i>\n'
                f'<b>├ Metadata: </b><i>{Similar["Solana"][2]}%</i>\n'
                f'<b>├ Website: </b><i>{Similar["Website"][2]}%</i>\n'
                f'<b>├ Telegram: </b><i>{Similar["Telegram"][2]}%</i>\n'
                f'<b>└ Twitter: </b><i>{Similar["Twitter"][2]}%</i>'
                f'</blockquote>\n')
    else:
        return ''

def CreateKeyboard(Token):
    Keyboard = []
    if Token['Address']:Keyboard.append([{"text": "Dexscreener", "url": f"https://dexscreener.com/solana/{Token['Address']}"},{"text": "Solscan", "url": f"https://solscan.io/token/{Token['Address']}"}, {"text": "Photon", "url": f"https://photon-sol.tinyastro.io/en/lp/{Token['Address']}"}])
    if Token['Data']['Website']: Keyboard.append([{"text": "Website", "url": Token['Data']['Website']['Site']['Url']['Full']}])
    if Token['Data']['Telegram']: Keyboard.append([{"text": "Telegram", "url": Token['Data']['Telegram']['Site']['Url']['Full']}])
    if Token['Data']['Twitter']: Keyboard.append([{"text": "Twitter", "url": Token['Data']['Twitter']['Site']['Url']['Full']}])
    if Token['Data']['Discord']: Keyboard.append([{"text": "Discord", "url": Token['Data']['Discord']['Site']['Url']['Full']}])
    return Keyboard

def Parse(Token):
    Data = {}
    Data['Address'] = Token['Address']
    Data['TopicId'] = Token['Owner']['Id']
    Data['TopicPostId'] = Token.get('TopicPostId')
    Data['TopicLastPostId'] = Token.get('TopicLastPostId')
    Data['GeneralPostId'] = Token.get('GeneralPostId')
    Data['Similar'] = Token['Owner'].get('Similarity')
    Data['Duplicate'] = Token.get('Duplicate')
    Data['Socials'] = Token['Data'].get('Website') or Token['Data'].get('Telegram') or Token['Data'].get('Twitter') or Token['Data'].get('Discord')
    Data['Name'] = Token['Data']['Solana']['Metaplex']['data']['name']
    Data['Symbol'] = Token['Data']['Solana']['Metaplex']['data']['symbol']
    Data['Decimals'] = Token['Data']['Solana']['Mint']['decimals']
    Data['Supply'] = f"{int(Token['Data']['Solana']['Mint']['supply'] / 10**Data['Decimals']):,}".replace(",", ".")
    Data['Mintable'] = bool(Token['Data']['Solana']['Mint']['mint_authority_option'])
    Data['Freezable'] = bool(Token['Data']['Solana']['Mint']['freeze_authority_option'])
    Data['Mutable'] = bool(Token['Data']['Solana']['Metaplex']['is_mutable'])
    Data['Uri'] = System.Url.Parse(Token['Data']['Solana']['Metaplex']['data']['uri'])['Domain']['Full']
    Data['Fee'] = Token['Data']['Solana']['Metaplex']['data']['seller_fee_basis_points']
    Data['Owner'] = Token['Data']['Solana']['Metaplex']['update_authority'].decode('utf-8')
    Data['OwnerBalance'] = Token['Data']['Solana']['Account'].get('Balance') or 0

    Creator = Token['Data']['Solana'].get('Metadata', {}).get('creator', {})
    if Creator:
        Data['CreatorName'] = Token['Data']['Solana']['Metadata']['creator'].get('name')
        Data['CreatorUrl'] = Token['Data']['Solana']['Metadata']['creator'].get('site') or Token['Data']['Solana']['Metadata']['creator'].get('url')
    else:
        Creator = Token['Data']['Solana'].get('Metadata', {}).get('createdOn', {})
        if Creator:
            Data['CreatorName'] =System.Url.Parse(Token['Data']['Solana']['Metadata']['createdOn'])['Domain']['Full']
            Data['CreatorUrl'] = Token['Data']['Solana']['Metadata']['createdOn']
        else:
            Data['CreatorName'] = 'None'
            Data['CreatorUrl'] = None

    Description = Token['Data']['Solana'].get('Metadata', {}).get('description', {})
    Data['Description'] = Description if Description else 'No description available'
    Tags = Token['Data']['Solana'].get('Metadata', {}).get('tags', {})
    Data['Tags'] = ' '.join(f'#{t}' for t in Tags) if Tags else ''

    return Data

def GetPreview(Token):
    File = f'{Token["Address"]}.png'
    return File if os.path.isfile(os.path.join('Previews',f'{File}')) else None

def SendPost(Topic,Message,Preview,Keyboard=None):
    if Preview:return Telegram.Bot.sendPhoto(Topic, os.path.join('Previews',f'{Preview}'), Message, Keyboard)
    else:return Telegram.Bot.sendMessage(Topic, Message, Keyboard)


