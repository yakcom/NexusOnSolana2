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


def NewRaydiumTokens(Address):
    logger.info(f'New Raydium Token {Address}')
    Token = {'Address':Address,'Date':datetime.now(),'Data':{}}

    if not Parsers.Solana.Parse(Token):return
    Parsers.Socials.Find(Token)
    Parsers.Website.Parse(Token)
    Parsers.Telegram.Parse(Token)
    Parsers.Twitter.Parse(Token)
    Parsers.Discord.Parse(Token)

    Comparison.Model.Create(Token)
    Similar = Comparison.Comparator.FindSimilar(Token,Database.RaydiumTokens)
    Comparison.Owner.Set(Token, Similar)

    Telegram.Notify.Parse(Token)
    Telegram.Group.Post(int(Config.Get('Telegram','NewRaydiumTokens')),Token)

    if Token['Notify']['Similar'] and not Token.get('Duplicate'):
        Telegram.Bot.forwardTopicMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewRaydiumTokensWithHistory')))
    if Token['Notify']['Safe']:
        Telegram.Bot.forwardTopicMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewRaydiumTokensSafe')))
    if Token['Owner']['Id'] == 16563:
        Telegram.Bot.forwardMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'GoldChannel')))

    del Token['Data']
    Database.SaveRaydiumToken(Token)
    logger.success(f'Success Raydium Token {Address}')


def NewRaydiumPools(Address):
    logger.info(f'New Raydium Pool {Address}')
    if Token := Database.RaydiumTokens.get(Address):
        Telegram.Bot.forwardTopicMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewRaydiumPools')))
        logger.success(f'Success Raydium Pool {Address}')


def NewPumpfunTokens(Address):
    logger.info(f'New Pumpfun Token {Address}')
    Token = {'Address': Address, 'Date': datetime.now(), 'Data': {}}

    if not Parsers.Solana.Parse(Token):return
    Parsers.Socials.Find(Token)
    Parsers.Website.Parse(Token)
    Parsers.Telegram.Parse(Token)
    Parsers.Twitter.Parse(Token)
    Parsers.Discord.Parse(Token)

    Comparison.Model.Create(Token)
    Similar = Comparison.Comparator.FindSimilar(Token, Database.PumpfunTokens)
    Comparison.Owner.Set(Token, Similar)

    Telegram.Notify.Parse(Token)
    Telegram.Group.Post(int(Config.Get('Telegram', 'NewPumpfunTokens')), Token)

    #TODO

    del Token['Data']
    Database.SavePumpfunToken(Token)
    logger.success(f'Success Pumpfun Token {Address}')