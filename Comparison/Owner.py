from loguru import logger
import Telegram.Bot

def Set(Token, Similar):
    logger.debug(f'Token owner determination for {Token["Address"]}')
    Token['Owner'] = {}
    if Similar:
        Token['Owner']['Id'] = Similar['Token']['Owner']['Id']
        Token['TopicLastPostId'] = Similar['Token']['TopicPostId']
        Token['Owner']['Similarity'] = Similar['Compare']
    else:
        TopicId = Telegram.Bot.createAndClose('Developer')
        Token['Owner']['Id'] = TopicId
        Telegram.Bot.editForumTopic(TopicId, f'Developer {TopicId}')