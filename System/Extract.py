import Parsers.Solana
import System.Url
import re

def SolanaAddresses(Message,Index=-1):
    Addresses = re.findall('[1-9A-HJ-NP-Za-km-z]{32,44}', Message)
    if Index>=0:return Addresses[Index] if Index < len(Addresses) else None
    else:return Addresses

def Socials(Urls):
    Website, Telegram, Twitter, Discord = None, None, None, None
    for Url in Urls:
        Domain = System.Url.Parse(Url)['Domain']['Full']
        TELEGRAM = ['t.me', 'telegram.me', 'telegram.org']
        if any(T == Domain for T in TELEGRAM): Telegram = Url;continue
        TWITTER = ['x.com', 't.co', 'twttr.com', 'twitter.com', 'twitterinc.com']
        if any(T == Domain for T in TWITTER): Twitter = Url;continue
        DISCORD = ['discord.gg', 'discord.com', 'discordapp.com', 'discordstatus.com']
        if any(D == Domain for D in DISCORD): Discord = Url;continue
        Website = Url;continue
    return {'Website':Website,'Telegram':Telegram,'Twitter':Twitter,'Discord':Discord}

def isWebsite(Url):
    return not (isTelegram(Url) or isTwitter(Url) or isDiscord(Url))

def isTelegram(Url):
    Domain = System.Url.Parse(Url)['Domain']['Full']
    TELEGRAM = ['t.me', 'telegram.me', 'telegram.org']
    return any(T == Domain for T in TELEGRAM)

def isTwitter(Url):
    Domain = System.Url.Parse(Url)['Domain']['Full']
    TWITTER = ['x.com', 't.co', 'twttr.com', 'twitter.com', 'twitterinc.com']
    return any(T == Domain for T in TWITTER)

def isDiscord(Url):
    Domain = System.Url.Parse(Url)['Domain']['Full']
    DISCORD = ['discord.gg', 'discord.com', 'discordapp.com', 'discordstatus.com']
    return any(D == Domain for D in DISCORD)



