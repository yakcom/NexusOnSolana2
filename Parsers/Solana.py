from spl.token._layouts import MINT_LAYOUT,ACCOUNT_LAYOUT
from solana.rpc.api import Client, PublicKey
from metaplex.metadata import get_metadata
from datetime import datetime
from loguru import logger
import requests,time,base64
import Config

Solana = None
def Init(Rpc):
    global Solana
    Solana = Client(Rpc)
    if Solana.is_connected():logger.debug('Solana rpc connected')
    else:logger.critical('Solana rpc error');exit()

def GetInformation(Address):
    Error = None
    logger.trace(f'Get information for {Address}')
    for a in range(60):
        try:
            Pubkey = PublicKey(Address)
            Response = Solana.get_account_info(Pubkey)
            Response = Response["result"]["value"]["data"][0]
            Layout = MINT_LAYOUT.parse(base64.b64decode(Response))
            Layout['mint_authority'] = str(PublicKey(Layout['mint_authority']))
            Layout['freeze_authority'] = str(PublicKey(Layout['freeze_authority']))
            return Layout
        except Exception as e:Error = e
        time.sleep(1)
    logger.error(f'{Address} Get information error {Error}')
    return


def GetMetaplex(Address):
    Error = None
    logger.trace(f'Get metaplex for {Address}')
    for a in range(60):
        try:return get_metadata(Solana, Address)
        except Exception as e:Error=e
        time.sleep(1)
    logger.error(f'{Address} Get metaplex error {Error}')
    return

def GetMetadata(Address):
    Error = None
    logger.trace(f'Get metadata for {Address}')
    for a in range(5):
        try:
            url = get_metadata(Solana, Address)['data']['uri']
            return requests.get(url).json()
        except Exception as e:Error=e
        time.sleep(1)
    logger.warning(f'{Address} Get metadata error {Error}')
    return

def GetAccount(Address):
    Error = None
    logger.trace(f'Get account for {Address}')
    for a in range(3):
        try:
            Pubkey = PublicKey(Address)
            Balance = round(Solana.get_balance(Pubkey)["result"]["value"]/10**9,2)
            #Transactions = Solana.get_signatures_for_address(Pubkey)["result"]
            #TransactionsCount = len(Transactions)
            #Age = datetime.utcnow()-datetime.utcfromtimestamp(Transactions[-1]['blockTime'])
            return {'Balance':Balance}
        except Exception as e:Error=e
        time.sleep(1)
    logger.warning(f'{Address} Get accuunt error {Error}')
    return

def Parse(Token):

    Token['Data']['Solana'] = {}
    Address = Token['Address']

    logger.debug(f'Solana parse for {Address}')

    if not (Information := GetInformation(Address)): return
    Token['Data']['Solana']['Mint'] = Information
    if not (Metaplex := GetMetaplex(Address)): return
    Token['Data']['Solana']['Metaplex'] = Metaplex
    if not (Metadata := GetMetadata(Address)): pass
    Token['Data']['Solana']['Metadata'] = Metadata or {}

    if Metaplex['mint'] != Metaplex['update_authority']:
        Token['Data']['Solana']['Account'] = GetAccount(Metaplex['update_authority'].decode('utf-8')) or {}
    else:
        Token['Data']['Solana']['Account'] =  {}

    return True
