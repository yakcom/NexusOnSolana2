from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from loguru import logger
import requests,time,pytz
import Database,Config
import Telegram.Bot as Telegram

Dexapi='https://api.dexscreener.com/latest/dex/tokens/'
def GetTokenInfo(address):
    try:return requests.get(Dexapi+address).json()['pairs'][0]
    except:return None

def GetDailyTokens(day,history=False):
    daily = []
    for token in Database.RaydiumTokens:
        if Database.RaydiumTokens[token]['Date'].date() == datetime.now().date()-timedelta(days=-1*day):
            if not history or Database.RaydiumTokens[token]['Owner'].get('Similarity'):
                daily.append(Database.RaydiumTokens[token])
    return daily

def ShowBestOfDay(day=-1):
    logger.info(f'Best of day {(datetime.now() - timedelta(days=-1*day)).strftime("%d.%m.%Y")} analysis')
    Tokens = GetDailyTokens(day, True)

    TokensWithInfo = []
    for token in Tokens:
        Dexscreener = GetTokenInfo(token['Address'])
        if (Dexscreener and Dexscreener.get('liquidity', {}).get('usd')):
            token['Dexscreener'] = Dexscreener
            TokensWithInfo.append(token)

    TokensWithInfo = sorted(TokensWithInfo, key=lambda item: item['Dexscreener']['liquidity']['usd'], reverse=False)

    Topic = Telegram.createAndClose("Best of " + (datetime.now() - timedelta(days=-1*day)).strftime("%d.%m.%Y"),'5433614043006903194')

    TokensWithInfo = TokensWithInfo[-10:]
    for token in TokensWithInfo:
        Telegram.forwardTopicMessage(token['GeneralPostId'], Topic)
        time.sleep(5)
    logger.success(f'Best of day {(datetime.now() - timedelta(days=-1*day)).strftime("%d.%m.%Y")} posted')


def ScheduleStatistics(hour,minute):
    Scheduler = BackgroundScheduler()
    Scheduler.add_job(ShowBestOfDay, 'cron', hour=hour, minute=minute, timezone=pytz.timezone('Europe/Moscow'))
    Scheduler.start()





