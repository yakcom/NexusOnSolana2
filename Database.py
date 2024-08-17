from loguru import logger
import os,pickle

RaydiumTokens = {}
PumpfunTokens = {}

def Loads(Directory):
    Tokens = {}
    for Address in os.listdir(Directory):
        TokenPath = os.path.join(Directory, Address)
        with open(TokenPath, 'rb') as TokenFile:
            Tokens[Address] = pickle.load(TokenFile)
    return Tokens

def Saves(Token, Directory):
    TokenPath = os.path.join(Directory, Token['Address'])
    with open(TokenPath, 'wb') as TokenFile:
        pickle.dump(Token, TokenFile)

def Load():
    global RaydiumTokens,PumpfunTokens
    RaydiumTokens = Loads('Database\Raydium')
    PumpfunTokens = Loads('Database\Pumpfun')
    logger.debug('Database loaded successfully')

def SaveRaydiumToken(Token):
    RaydiumTokens[Token['Address']] = Token
    Saves(Token, 'Database\Raydium')
    logger.debug(f'Raydium token saved {Token["Address"]}')

def SavePumpfunToken(Token):
    PumpfunTokens[Token['Address']] = Token
    Saves(Token, 'Database\Pumpfun')
    logger.debug(f'Pumpfun token saved {Token["Address"]}')



