from loguru import logger
import Telegram.Bot,os
import Telegram.Group

def Post(Topic,Token):
    logger.trace(f'General post {Token["Address"]}')
    Preview = Telegram.Group.GetPreview(Token)
    Info = Telegram.Group.Parse(Token)

    HeaderBar = Telegram.Group.CreateHeaderBar(Info)
    TokenBar = Telegram.Group.CreateTokenBar(Info)
    NotifyBar = Telegram.Group.CreateNotifyBar(Info)
    AddressBar = Telegram.Group.CreateAddressBar(Info)
    TagsBar = Telegram.Group.CreateTagsBar(Info)
    Keyboard = Telegram.Group.CreateKeyboard(Token)

    Message = f'{HeaderBar}{TokenBar}{NotifyBar}{AddressBar}{TagsBar}'

    for a in range(3):
        Post = Telegram.Group.SendPost(Topic, Message, Preview, Keyboard)
        if Post and Post['ok']:Token['GeneralPostId'] = Post['result']['message_id'];return
        else:
            logger.warning(f'General post error for {Token["Address"]}')

