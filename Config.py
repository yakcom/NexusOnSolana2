from configparser import ConfigParser
from loguru import logger

Config=None

def Load(File='Config.ini'):
    global Config
    Config=ConfigParser()
    Config.read(File)
    logger.debug('Configuration loaded successfully')

def Get(Section,Option):
    if not Config:logger.critical('Configuration file not initialized');exit()
    try:return Config.get(Section,Option)
    except:return None