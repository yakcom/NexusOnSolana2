from loguru import logger
import requests

Api = 'bot6409923201:AAH8UXDC1HWyJGn91_USD80wLjuXY0RUx9w'

def Parse(Token):

    if not (Telegram := Token['Data']['Telegram']):return
    logger.debug(f'Telegram parse for {Token["Address"]}')
    Name = Telegram['Site']['Url']['Full'].split('/')[-1]

    logger.trace(f'Request chat @{Name}')
    Response = requests.get(f'https://api.telegram.org/{Api}/getChat', params={'chat_id': f'@{Name}'})
    if(Response.status_code == 200):Telegram['Chat'] = Response.json()['result']
    else:Token['Data']['Telegram']=None