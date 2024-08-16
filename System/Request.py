from loguru import logger
import requests,warnings,time
warnings.filterwarnings("ignore")

Header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

def Get(Url,Attempts=3,Delay=5):
    Error = None
    logger.trace(f'Request to {Url}')
    for a in range(Attempts):
        try:
            Response = requests.get(Url, verify=False, headers=Header)
            if Response.status_code == 200:return Response
            else:Error=ValueError(f'{Url} bad status code: {Response.status_code}')
        except Exception as e:Error=ValueError(f'{Url} request error: {e}')
        time.sleep(Delay)
    raise Error