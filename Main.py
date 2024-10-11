import Config,Database,Core,Statistics
from Parsers import Solana
from loguru import logger
import Comparison.Model
import Telegram.Bot
import Telethon.Bot,sys

logger.remove()
logger.add(sys.stderr, level="TRACE")
logger.info('Nexus On Solana 2')

Config.Load()
Database.Load()
Comparison.Model.Load()

Statistics.ScheduleStatistics(00,00)

Solana.Init(Config.Get('Solana','Rpc'))
Telegram.Bot.Init(Config.Get('Telegram','Token'),Config.Get('Telegram','Group'))

Telethon.Bot.Subscribe(Core.NewRaydiumTokens, Config.Get('Telethon', 'NewRaydiumTokens').split(','))
Telethon.Bot.Subscribe(Core.NewRaydiumPools, Config.Get('Telethon', 'NewRaydiumPools').split(','))
#Telethon.Bot.Subscribe(Core.NewPumpfunTokens, Config.Get('Telethon', 'NewPumpfunTokens').split(','))

Telethon.Bot.Start()