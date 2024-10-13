from datetime import datetime
from loguru import logger

import Config
import Database

import Telegram.Bot
import Telegram.Group
import Telegram.Notify

import Parsers.Solana
import Parsers.Socials
import Parsers.Website
import Parsers.Telegram
import Parsers.Twitter
import Parsers.Discord

import Comparison.Model
import Comparison.Comparator
import Comparison.Owner


def NewTokens(Address):
    Dex = Config.Get("Nexus","Dex")
    logger.info(f'New {Dex} Token {Address}')

    Token = {'Address':Address,'Date':datetime.now(),'Data':{}}

    if not Parsers.Solana.Parse(Token):return
    Parsers.Socials.Find(Token)
    Parsers.Website.Parse(Token)
    Parsers.Telegram.Parse(Token)
    Parsers.Twitter.Parse(Token)
    Parsers.Discord.Parse(Token)

    if eval(Config.Get('Nexus','OnlyWithWebsites')) and not Token['Data']['Website']:
        logger.warning(f'No Website {Dex} Token {Address}')
        return

    Comparison.Model.Create(Token)
    Similar = Comparison.Comparator.FindSimilar(Token)
    Comparison.Owner.Set(Token, Similar)

    Telegram.Notify.Parse(Token)
    Telegram.Group.Post(int(Config.Get('Telegram','NewTokens')),Token)

    if Token['Notify']['Similar'] and not Token.get('Duplicate') and eval(Config.Get('Nexus','ForwardToTokensWithHistory')):
        Telegram.Bot.forwardTopicMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewTokensWithHistory')))
    if Token['Notify']['Safe'] and eval(Config.Get('Nexus','ForwardToTokensSafe')):
        Telegram.Bot.forwardTopicMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewTokensSafe')))

    if Token['Owner']['Id'] == 16563:
        Telegram.Bot.forwardMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'GoldChannel')))

    del Token['Data']
    Database.Save(Token)
    logger.success(f'Success {Dex} Token {Address}')


def NewPools(Address):
    Dex = Config.Get("Nexus", "Dex")
    if Token := Database.Tokens.get(Address):
        Telegram.Bot.forwardTopicMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewPools')))
        logger.success(f'Success {Dex} Pool {Address}')