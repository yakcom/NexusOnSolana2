from loguru import logger
import Telegram.Bot,os
import Telegram.Group
import Config

def Post(Token):
    logger.trace(f'Topic post {Token["Address"]}')
    Preview = Telegram.Group.GetPreview(Token)
    Info = Telegram.Group.Parse(Token)

    HeaderBar = CreateHeaderBar(Info)
    TokenBar = Telegram.Group.CreateTokenBar(Info)
    ComparisonBar = Telegram.Group.CreateComparisonBar(Info)
    NotifyBar = CreateNotifyBar(Info)
    AddressBar = Telegram.Group.CreateAddressBar(Info)
    TagsBar = Telegram.Group.CreateTagsBar(Info)
    Keyboard = Telegram.Group.CreateKeyboard(Token)

    Message = f'{HeaderBar}{TokenBar}{ComparisonBar}{NotifyBar}{AddressBar}{TagsBar}'

    for a in range(3):
        Post = Telegram.Group.SendPost(Info['TopicId'], Message, Preview, Keyboard)
        if Post and Post['ok']:Token['TopicPostId'] = Post['result']['message_id'];return
        else:
            logger.warning(f'Topic post error for {Token["Address"]}')

def CreateHeaderBar(Info):
    return (f'<blockquote>'
            f'<b><a href="https://t.me/c/{Telegram.Bot.Group}/{Info["TopicId"]}">{Info["Name"].strip().capitalize()}</a></b>\n'
            f'<i>{Info["Description"].strip()}</i>'
            f'</blockquote>\n')

def CreateNotifyBar(Info):
    Notify=[]
    if Info['Duplicate']: Notify.append(f'<blockquote><b>⚠️  <a href="https://t.me/c/{Telegram.Bot.Group}/{Config.Get("Telegram","NewRaydiumTokens")}/{Info["Duplicate"]}">Such token already exists</a></b></blockquote>')
    if Info['Freezable']: Notify.append('<blockquote><b>⛔️  Token sale is not possible</b></blockquote>')
    if Info['Mintable']: Notify.append('<blockquote><b>⚠️  Developer can mint more</b></blockquote>')
    if Info['Mutable']: Notify.append('<blockquote><b>⚠️  Developer can change token</b></blockquote>')
    if Info['OwnerBalance'] == 0: Notify.append('<blockquote><b>⚠️  Developer has zero balance</b></blockquote>')
    if not Info['Socials']: Notify.append('<blockquote><b>⚠️  Socials not found</b></blockquote>')
    Notify = '\n'.join(Notify)
    if Notify:return f'{Notify}\n'
    else:return ''