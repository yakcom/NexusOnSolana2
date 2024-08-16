from loguru import logger
import System.Request
import System.Selenium
import System.Metadata
import System.Whois
import System.Ip


def Parse(Token):
    if not (Website := Token['Data']['Website']):return
    logger.debug(f'Website parse for {Token["Address"]}')
    Url = Website['Site']['Url']['Full']

    try:Website['Request'] = System.Request.Get(Url)
    except Exception as e:logger.warning(e);Token['Data']['Website']=None;return
    try:Website['Html'] = Html = System.Selenium.Get(Url,Token)
    except Exception as e:logger.warning(e);Token['Data']['Website']=None;return
    try:Website['Meta'] = System.Metadata.Get(Url,Html)
    except Exception as e:logger.warning(e);Token['Data']['Website']=None;return
    try:Website['Ip'] = System.Ip.Get(Url)
    except Exception as e:logger.warning(e);Token['Data']['Website']=None;return
    try:Website['Whois'] = System.Whois.Get(Url)
    except Exception as e:logger.warning(e);Token['Data']['Website']=None;return


    