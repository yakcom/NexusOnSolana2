from loguru import logger
import os,pickle

Tokens = {}

def Load(dir='Database'):
    global Tokens
    for address in os.listdir(dir):
        with open(os.path.join(dir, address), 'rb') as file:
            Tokens[address] = pickle.load(file)
    logger.debug('Database loaded successfully')

def Save(Token,dir='Database'):
    global Tokens
    with open(os.path.join(dir, Token['Address']), 'wb') as file:
        pickle.dump(Token, file)
    logger.debug(f'Token saved {Token["Address"]}')



