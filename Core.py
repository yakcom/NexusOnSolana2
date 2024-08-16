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
    Similar = Comparison.Comparator.FindSimilar(Token)
    Comparison.Owner.Set(Token, Similar)

    Telegram.Notify.Parse(Token)
    Telegram.Group.Post(int(Config.Get('Telegram','NewRaydiumTokens')),Token)

    if Token['Notify']['Similar'] and not Token.get('Duplicate'):
        Telegram.Bot.forwardMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewRaydiumTokensWithHistory')))
    if Token['Notify']['Safe']:
        Telegram.Bot.forwardMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewRaydiumTokensSafe')))

    del Token['Data']
    Database.Save(Token)
    logger.success(f'Success Raydium Token {Address}')


def NewRaydiumPools(Address):
    logger.info(f'New Raydium Pool {Address}')
    if Token := Database.Tokens.get(Address):
        Telegram.Bot.forwardMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewRaydiumPools')))
        logger.success(f'Success Raydium Pool {Address}')
    else:
        logger.warning(f'Raydium Token {Address} missing from database')

