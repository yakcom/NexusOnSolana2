from loguru import logger
import requests,json

#------------------------
Url = 'api.telegram.org'
Token = None
Group = None
Chat =  None
#------------------------

def Init(token,group):
    global Group;Group=group
    global Chat;Chat='-100'+group
    global Token;Token=token
    if Request('getMe')['ok']:logger.debug('Telegram bot connected')
    else:logger.critical('Telegram bot initialization error');exit()

def Request(Method,Data=None,Files=None):
    if not Token:raise Exception('Telegram is not initialized !')
    return requests.post(f'https://{Url}/bot{Token}/{Method}', data=Data,files=Files).json()

def createForumTopic(Name):
    Data = {'chat_id': Chat, 'name': Name}
    return Request('createForumTopic',Data)

def closeForumTopic(Thread):
    Data = {'chat_id': Chat, 'message_thread_id': Thread}
    return Request('closeForumTopic', Data)

def editForumTopic(TopicId, Name):
    Data = {'chat_id': Chat, 'message_thread_id': TopicId, 'name':Name}
    return Request('editForumTopic', Data)

def createAndClose(Name):
    Topic = createForumTopic(Name)
    TopicId = Topic['result']['message_thread_id']
    closeForumTopic(TopicId)
    return TopicId

def forwardMessage(MessageFrom, TopicTo):
    Data = {
        'chat_id': Chat,
        'message_thread_id':TopicTo,
        'from_chat_id': Chat,
        'message_id': MessageFrom
    }
    return Request('forwardMessage', Data)

def sendMessage(Topic, Message, Keyboard=None, Silently=False, Markdown='Html', Preview=False):
    if Keyboard: Keyboard = json.dumps({"inline_keyboard": Keyboard})
    Data = \
        {
            'chat_id': Chat,
            'text': Message,
            'parse_mode': Markdown,
            'reply_markup': Keyboard,
            'disable_web_page_preview':not Preview,
            'disable_notification':Silently
        }
    if Topic > 0: Data['message_thread_id'] = Topic
    return Request('sendMessage', Data)

def sendPhoto(Topic, Photo, Message, Keyboard=None, Silently=False, Markdown='Html'):
    if Keyboard:Keyboard = json.dumps({"inline_keyboard": Keyboard})
    Data = \
        {
            'chat_id': Chat,
            'caption': Message,
            'parse_mode': Markdown,
            'reply_markup': Keyboard,
            'disable_notification':Silently
        }
    if Topic>0:Data['message_thread_id'] = Topic
    File=None
    if '://' in Photo:Data['photo'] = Photo
    else:File = {'photo':open(Photo,'rb')}
    return Request('sendPhoto', Data,File)

#Init('7462587727:AAGZ-vyyQsg9iuOhHzDqslKOB8vAgoCDpUM')
