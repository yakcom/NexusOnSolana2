import Comparison.Comparator
import Config
import Database
import json
import requests
import Comparison.Comparator

Config.Load()

x = Config.Get('Nexus','ForwardToTokensSafe')


Database.Load()
x= Database.Tokens
Whois1 = x['27ssXpvwBpjXWpkutqNjjtGxZqNgc6bbpu8zRp3Uv3t5']['Model']['Website']['Headers']
Whois2 = x['ByLspEWQCg3RVdqc5ZH9eeG57LPyh3jtVTTPzKBhapiP']['Model']['Website']['Headers']
y= Comparison.Comparator.СompareDictionaryesPercentages(Whois1,Whois2)
v=32