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
    logger.info(f'New Pumpfun Token {Address}')

    Token = {'Address':Address,'Date':datetime.now(),'Data':{}}

    if not Parsers.Solana.Parse(Token):return
    Parsers.Socials.Find(Token)
    Parsers.Website.Parse(Token)
    if not Token['Data']['Website']:logger.warning(f'No Website Pumpfun Token {Address}');return
    Parsers.Telegram.Parse(Token)
    Parsers.Twitter.Parse(Token)
    Parsers.Discord.Parse(Token)

    Comparison.Model.Create(Token)
    Similar = Comparison.Comparator.FindSimilar(Token)
    Comparison.Owner.Set(Token, Similar)

    Telegram.Notify.Parse(Token)
    Telegram.Group.Post(int(Config.Get('Telegram','NewTokens')),Token)

    if Token['Notify']['Similar'] and not Token.get('Duplicate'):
        Telegram.Bot.forwardTopicMessage(Token['GeneralPostId'], int(Config.Get('Telegram', 'NewTokensWithHistory')))

    del Token['Data']
    Database.Save(Token)

    logger.success(f'Success Pumpfun Token {Address}')