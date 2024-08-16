from telethon.sync import TelegramClient, events
from loguru import logger
import asyncio,threading
import System.Extract
import Config

Subscriptions = []
def Subscribe(Event,Subs):
    Subscriptions.append((Event,Subs))

def Start():
    async def Start():
        Id = Config.Get("Telethon", "Id")
        Hash = Config.Get("Telethon", "Hash")
        Telethon = TelegramClient('Telethon/Account', Id, Hash)
        await Telethon.start()

        global Subscriptions
        Subscriptions = [(Subscription[0], {(await Telethon.get_entity(Username)).id: Username for Username in Subscription[1]})for Subscription in Subscriptions]

        logger.debug('Telethon client connected')
        logger.success('Nexus On Solana 2')

        @Telethon.on(events.NewMessage())
        async def NewMessage(event):
            try:Chat,Message = event.chat.id,event.message.message
            except:return

            for Subscription in Subscriptions:
                if Subscription[1].get(Chat) in ['@SolanaMintsDebug2','@DRBTSolana','@solanapoolsnew','@SolanaPoolsDebug2','@NewToken_Sol']:
                    if Address := System.Extract.SolanaAddresses(Message, 0):
                        threading.Thread(target=Subscription[0], args=(Address,)).start()
                if Subscription[1].get(Chat) in ['@NewPoolSolana']:
                    if Address := System.Extract.SolanaAddresses(Message, 1):
                        threading.Thread(target=Subscription[0], args=(Address,)).start()

        await Telethon.run_until_disconnected()
    asyncio.run(Start())
