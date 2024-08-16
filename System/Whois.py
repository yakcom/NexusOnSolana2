from loguru import logger
import whois,time

def Get(Url):
    Error = None
    logger.trace(f'Get whois for {Url}')
    for a in range(3):
        try:return whois.whois(Url)
        except Exception as e:Error = ValueError(f'{Url} whois error {e}');
        time.sleep(5)
    raise Error