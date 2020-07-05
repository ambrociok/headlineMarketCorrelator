import requests
import json

#Oh my god these are some garbage APIS


def getEODData():
    changes = []
    tickersToSearchFor = ['IXIC', 'DJI', 'INX', 'QQQ']
#    for ticker in tickersToSearchFor:
    url = ('https://financialmodelingprep.com/api/v3/historical-price-full/DJI?serietype=line&apikey=de57a4c918c79866cabc658cc4e774bd')
    response = requests.get(url).json() #.format(ticker)
    print(response)
#        changes.append([ticker, response['open'], response['close'], response['changePercent']])
    return changes

def getHistorical():
    historical = []
    tickersToSearchFor = ['IXIC', 'DJI', 'SP500TR']
    for ticker in tickersToSearchFor:
        url = ('https://financialmodelingprep.com/api/v3/historical-price-full/{}?apikey=de57a4c918c79866cabc658cc4e774bd')
        r = requests.get(url.format(ticker)).json()
        print()
        historical.append(r['historical']['date'], r['historical']['open'], r['historical']['close'], r['historical']['changePercent'])
    return historical