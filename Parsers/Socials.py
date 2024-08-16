from loguru import logger
import System.Dictionary
import System.Download
import System.Extract
import System.Url

def Find(Token):
    Address = Token['Address']
    logger.debug(f'Find socials for {Address}')
    Token['Data']['Website'],Token['Data']['Telegram'],Token['Data']['Twitter'],Token['Data']['Discord'] =  [None]*4
    Website1,Website2,Telegram1,Telegram2,Twitter1,Twitter2,Discord1,Discord2 = [None]*8

    if (Metadata := Token['Data']['Solana']['Metadata']):
        logger.trace(f'Find socials in metadata for {Address}')
        Website1 = System.Url.Parse(System.Dictionary.DeepFind(Metadata, 'website'))
        Telegram1 = System.Url.Parse(System.Dictionary.DeepFind(Metadata, 'telegram'))
        Twitter1 = System.Url.Parse(System.Dictionary.DeepFind(Metadata, 'twitter'))
        Discord1 = System.Url.Parse(System.Dictionary.DeepFind(Metadata, 'discord'))

        if 'description' in Metadata:
            logger.trace(f'Find socials in description for {Address}')
            Websites = System.Url.Find(Metadata['description'])
            Socials = System.Extract.Socials(Websites)
            Website2 = System.Url.Parse(Socials['Website'])
            Telegram2 = System.Url.Parse(Socials['Telegram'])
            Twitter2 = System.Url.Parse(Socials['Twitter'])
            Discord2 = System.Url.Parse(Socials['Discord'])

    Website = Website1 or Website2
    Telegram = Telegram1 or Telegram2
    Twitter = Twitter1 or Twitter2
    Discord = Discord1 or Discord2

    if Website and System.Extract.isWebsite(Website['Url']['Full']): Token['Data']['Website'] = {'Site': Website}
    if Telegram and System.Extract.isTelegram(Telegram['Url']['Full']): Token['Data']['Telegram'] = {'Site': Telegram}
    if Twitter and System.Extract.isTwitter(Twitter['Url']['Full']): Token['Data']['Twitter'] = {'Site': Twitter}
    if Discord and System.Extract.isDiscord(Discord['Url']['Full']): Token['Data']['Discord'] = {'Site': Discord}

    if not Website:System.Download.Preview(Token)