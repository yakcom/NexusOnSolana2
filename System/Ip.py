from loguru import logger
import System.Url
import socket,time

def Get(Url):
    logger.trace(f'Get ip for {Url}')
    Name = System.Url.Parse(Url)['Url']['Short']
    Error=None
    for a in range(3):
        try:return socket.gethostbyname(Name)
        except Exception as e:Error=ValueError(f'{Url} ip error {e}');
        time.sleep(5)
    raise Error