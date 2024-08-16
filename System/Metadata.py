from bs4 import BeautifulSoup
from loguru import logger
import metadata_parser

def Get(Url,Html):
    try:
        Meta = {}

        logger.trace(f'Get metadata for {Url}')
        Page = metadata_parser.MetadataParser(html=Html)
        Soup = BeautifulSoup(Html, 'html.parser')

        try:Meta['Lang'] = str(Soup.find("html")["lang"])
        except:Meta['Lang'] = None

        Meta['Page'] = Page.metadata['page']
        Meta['Meta'] = Page.metadata['meta']
        Meta['Og'] = Page.metadata['og']
        Meta['Dc'] = Page.metadata['dc']
        Meta['Twitter'] = Page.metadata['twitter']

        return Meta
    except Exception as e:
        raise ValueError(f'{Url} metadata error {e}')