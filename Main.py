import Config,Database,Core,Statistics
from Parsers import Solana
from loguru import logger
import Comparison.Model
import Telethon.Bot
import Telegram.Bot
import sys

logger.remove()
logger.add(sys.stderr, level="TRACE")
logger.info('Nexus On Solana Pumpfun')

Config.Load()
Database.Load()
Comparison.Model.Load()

Statistics.ScheduleStatistics(00,00)

Solana.Init(Config.Get('Solana','Rpc'))
Telegram.Bot.Init(Config.Get('Telegram','Token'),Config.Get('Telegram','Group'))

Telethon.Bot.Subscribe(Core.NewTokens, Config.Get('Telethon', 'NewTokens').split(','))

Telethon.Bot.Start()