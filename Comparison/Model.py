from loguru import logger
import System.Url,json

Model = None

def Load(File='Model.json'):
    global Model
    try:
        with open(File, 'r') as f:
            Model = json.load(f)
        logger.debug('Model loaded successfully')
    except:logger.critical('Model not initialized');exit()


def Create(Token):
    logger.debug(f'Create comparison model for {Token["Address"]}')

    Model = {'Solana':{},'Website':{},'Telegram':{},'Twitter':{},'Discord':{}}

    Mint = Token['Data']['Solana']['Mint']# Mint Model
    # -----------------------------------------------------------------------------------------
    Model['Solana']['Init'] = bool(Mint['is_initialized'])
    Model['Solana']['Supply'] = int(Mint['supply'])
    Model['Solana']['Decimal'] = int(Mint['decimals'])
    Model['Solana']['Mintable'] = bool(Mint['mint_authority_option'])
    Model['Solana']['Freezable'] = bool(Mint['freeze_authority_option'])
    Model['Solana']['FreezeAuthority'] = str(Mint['freeze_authority']).lower()
    # -----------------------------------------------------------------------------------------
    Metaplex = Token['Data']['Solana']['Metaplex']# Metaplex Model
    # -----------------------------------------------------------------------------------------
    Model['Solana']['Name'] = bool(Metaplex['data']['name'].isupper())
    Model['Solana']['Symbol'] = bool(Metaplex['data']['symbol'].isupper())
    Model['Solana']['Name.$'] = bool('$' in Metaplex['data']['name'])
    Model['Solana']['Symbol.$'] = bool('$' in Metaplex['data']['symbol'])
    Model['Solana']['Uri'] = str(System.Url.Parse(Metaplex['data']['uri'])['Domain']['Full']) if System.Url.Parse(Metaplex['data']['uri']) else None
    Model['Solana']['Fee'] = int(Metaplex['data']['seller_fee_basis_points'])
    Model['Solana']['Creators'] = len(Metaplex['data']['creators'])
    Model['Solana']['Verified'] = len(Metaplex['data']['verified'])
    Model['Solana']['Share'] = len(Metaplex['data']['share'])
    Model['Solana']['Primary'] = bool(Metaplex['primary_sale_happened'])
    Model['Solana']['Mutable'] = bool(Metaplex['is_mutable'])
    Model['Solana']['SelfCreated'] = bool(Metaplex['update_authority'].lower()==Metaplex['mint'].lower())
    # -----------------------------------------------------------------------------------------

    Metadata = Token['Data']['Solana']['Metadata']# Metadata Model
    # -----------------------------------------------------------------------------------------
    if Metadata:
        Model['Solana']['Meta'] = len(Metadata)
        Model['Solana']['Image'] = str(System.Url.Parse(Metadata['image'])['Domain']['Full']) if Metadata.get('image') else None
        Model['Solana']['Description'] = bool(Metadata.get('description'))
        Model['Solana']['Extensions'] = len(Metadata['extensions']) if Metadata.get('extensions') else -1
        Model['Solana']['Tags'] = list(Metadata['tags']) if Metadata.get('tags') else []
        Model['Solana']['Creator'] = str(Metadata['creator']['name']) if Metadata.get('creator',{}).get('name') else None
        Model['Solana']['CreateOn'] = str(Metadata.get('createdOn'))
        Model['Solana']['ShowName'] = bool(Metadata.get('showName'))
    # -----------------------------------------------------------------------------------------

    Website = Token['Data']['Website']# Website Model
    # -----------------------------------------------------------------------------------------
    if Website:
        Model['Website']['Url'] =str(Website['Site']['Url']['Short'])
        Model['Website']['DomainZone'] = str(Website['Site']['Domain']['Zone'])
        Model['Website']['Protocol'] = str(Website['Site']['Protocol'])
        Model['Website']['Www'] = bool(Website['Site']['Www'])
        Model['Website']['Subdomains'] = len(Website['Site']['Subdomains'])
        Model['Website']['Paths'] = len(Website['Site']['Path'])
        Model['Website']['Encoding'] = str(Website['Request'].apparent_encoding)
        Model['Website']['Iso'] = str(Website['Request'].encoding)
        Model['Website']['Headers'] = dict(Website['Request'].headers)
        Model['Website']['Cookies'] = dict(Website['Request'].cookies)
        Model['Website']['Redirect'] = bool(Website['Request'].is_redirect)
        Model['Website']['PermRedirect'] = bool(Website['Request'].is_permanent_redirect)
        Model['Website']['Lang'] = str(Website['Meta']['Lang'])
        Model['Website']['Page'] = dict(Website['Meta']['Page'])
        Model['Website']['Meta'] = dict(Website['Meta']['Meta'])
        Model['Website']['Og'] = dict(Website['Meta']['Og'])
        Model['Website']['Dc'] = dict(Website['Meta']['Dc'])
        Model['Website']['Twitter'] = dict(Website['Meta']['Twitter'])
        Model['Website']['ContentType'] = str(Website['Meta']['Meta'].get('Content-Type'))
        Model['Website']['Viewport'] = str(Website['Meta']['Meta'].get('viewport'))
        Model['Website']['Descriptions'] = bool(Website['Meta']['Meta'].get('description'))
        Model['Website']['OgImageType'] = str(Website['Meta']['Meta'].get('og:image:type'))
        Model['Website']['TwitterCard'] = str(Website['Meta']['Meta'].get('twitter:card'))
        Model['Website']['Ip'] = str(Website['Ip'])
        Model['Website']['Whois'] = dict(Website['Whois'])
    # -----------------------------------------------------------------------------------------

    Telegram = Token['Data']['Telegram']# Telegram Model
    # -----------------------------------------------------------------------------------------
    if Telegram:
        Model['Telegram']['Url'] = str(Telegram['Site']['Domain']['Full'].lower())
        Model['Telegram']['Title.Keywords'] = list(Telegram['Chat']['title'].lower().split(' '))
        Model['Telegram']['Title.$'] = bool('$' in Telegram['Chat']['title'])
        Model['Telegram']['Type'] = str(Telegram['Chat'].get('type'))
        Model['Telegram']['Description'] = bool(Telegram['Chat'].get('description'))
        Model['Telegram']['PinnedMessage'] = bool(Telegram['Chat'].get('pinned_message'))
        Model['Telegram']['ActiveUsernames'] = len(Telegram['Chat'].get('active_usernames'))
        Model['Telegram']['HasVisibleHistory'] = bool(Telegram['Chat'].get('has_visible_history'))
        Model['Telegram']['CanSendPaidMedia'] = bool(Telegram['Chat'].get('can_send_paid_media'))
        Model['Telegram']['ReactionsAvailable'] = bool(Telegram['Chat'].get('available_reactions'))
        Model['Telegram']['MaxReactionCount'] = str(Telegram['Chat'].get('max_reaction_count'))
        Model['Telegram']['AccentColor'] = str(Telegram['Chat'].get('accent_color_id'))
    # -----------------------------------------------------------------------------------------

    Twitter = Token['Data']['Twitter']# Twitter Model
    # -----------------------------------------------------------------------------------------
    if Twitter:
        Model['Twitter']['Url'] = str(Twitter['Site']['Domain']['Full'].lower())
    # -----------------------------------------------------------------------------------------

    Discord = Token['Data']['Discord']# Discord Model
    # -----------------------------------------------------------------------------------------
    if Discord:
        Model['Discord']['Url'] = str(Discord['Site']['Domain']['Full'].lower())
    # -----------------------------------------------------------------------------------------

    Token['Model'] = Model