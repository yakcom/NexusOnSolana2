from loguru import logger
import Comparison.Model
import Database


def СompareDictionaryesPercentages(x,y):
    All = len(x.keys())
    Matches = sum(1 for k in x if k in y and x[k] == y[k])
    return int((Matches/All)*100)

def СompareDictionaryes(x, y):
    K = sum(1 for k in x if k in y)
    V = sum(1 for k in x if k in y and x[k] == y[k])
    return (K,V)

def CompareLists(x, y):
    L = sum(1 for k in x if k in y)
    return L


def CompareModels(Module,module,Model):
    All,Score,Percent = 0,0,0
    for Parameter in Module:

        try:
            Property = Module[Parameter]
            property = module[Parameter]
            Weight,Type = Model[Parameter]
        except:
            continue

        if Type==0:
            All+=Weight
            if Property == property:Score+=Weight
        if Type==1:
            All+=len(Property)*Weight
            Keys,Values = СompareDictionaryes(Property, property)
            Score += Keys * Weight
        if Type==2:
            All += len(Property) * Weight
            Keys,Values = СompareDictionaryes(Property, property)
            Score += Values * Weight
        if Type==3:
            All += len(Property) * Weight*2
            Keys,Values = СompareDictionaryes(Property, property)
            Score += Keys * Weight
            Score += Values * Weight
        if Type==4:
            All += len(Property) * Weight
            Values = CompareLists(Property, property)
            Score += Values * Weight
        if Type==5:
            if Property != property:return
        if Type==6:
            Value = СompareDictionaryesPercentages(Property, property)
            if Value < Weight:return

    Percent = int(Score/All*100) if All>0 else 0
    return Score,All,Percent



def FindSimilar(Token):
    logger.debug(f'Comparison of models for {Token["Address"]}')

    Model = Token['Model']
    Similar = {}

    if not (Model['Website'] and Model['Telegram']): return {}
    for address,token in Database.Tokens.items():
        if Token['Address'] == token['Address']:continue
        model = token['Model']

        if Model.get('Website') and model.get('Website'):
            if Model['Website']['Url']==model['Website']['Url']:
                if not Token.get('Duplicate'):
                    Token['Duplicate']=token['GeneralPostId']
                else:
                    if token['GeneralPostId'] > Token['Duplicate']:
                        Token['Duplicate'] = token['GeneralPostId']

        #if Token.get('Duplicate'): return {} #Do not add duplicates to the developer's history

        Compare = {}
        if not (model['Website'] and model['Telegram']): continue

        if not (Solana := CompareModels(Model['Solana'],model['Solana'],Comparison.Model.Model['Solana'])):continue
        if not (Website := CompareModels(Model['Website'], model['Website'],Comparison.Model.Model['Website'])):continue
        if not (Telegram := CompareModels(Model['Telegram'], model['Telegram'],Comparison.Model.Model['Telegram'])):continue
        if not (Twitter := CompareModels(Model['Twitter'], model['Twitter'],Comparison.Model.Model['Twitter'])):continue
        if not (Discord := CompareModels(Model['Discord'], model['Discord'],Comparison.Model.Model['Discord'])):continue

        Compare['Solana'] = Solana
        Compare['Website'] = Website
        Compare['Telegram'] = Telegram
        Compare['Twitter'] = Twitter
        Compare['Discord'] = Discord

        Compare['Score'] = Score = sum([Solana[0], Website[0], Telegram[0], Twitter[0], Discord[0]])
        Compare['All'] = All = sum([Solana[1], Website[1], Telegram[1], Twitter[1], Discord[1]])
        Compare['Percent'] = int(Score/All*100)

        if not Similar or Similar['Compare']['Score'] <= Compare['Score']:
            Similar['Token'] = token
            Similar['Compare'] = Compare

    return Similar



