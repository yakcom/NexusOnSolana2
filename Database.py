from loguru import logger
import os,pickle

Tokens = {}

def Load(Directory='Database'):
    for Address in os.listdir(Directory):
        TokenPath = os.path.join(Directory, Address)
        with open(TokenPath, 'rb') as TokenFile:
            Tokens[Address] = pickle.load(TokenFile)
    logger.debug('Database loaded successfully')

def Save(Token,Directory='Database'):
    Tokens[Token['Address']] = Token
    TokenPath = os.path.join(Directory, Token['Address'])
    with open(TokenPath, 'wb') as TokenFile:
        pickle.dump(Token, TokenFile)
    logger.debug(f'Token saved {Token["Address"]}')



