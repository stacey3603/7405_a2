import pandas as pd
import numpy as np


marketData = pd.read_csv('marketdata.csv', delimiter=',')
instruments = pd.read_csv('instruments.csv', delimiter=',')

marketData = marketData.to_dict('records')
instruments = instruments.to_dict('records')


def screenShot_31(Symbol):
    SymbolEntries = []
    for data in marketData:
        if data["Symbol"] == Symbol:
            if data['LocalTime'] < '2016-Feb-16 09:31:00':
                SymbolEntries.append(data)
    return SymbolEntries[-1:][0]


def screenShot_32(Symbol):
    SymbolEntries = []
    for data in marketData:
        if data["Symbol"] == Symbol:
            if data['LocalTime'] < '2016-Feb-16 09:32:00':
                SymbolEntries.append(data)
    return SymbolEntries[-1:][0]


def screenShot_33(Symbol):
    SymbolEntries = []
    for data in marketData:
        if data["Symbol"] == Symbol:
            if data['LocalTime'] < '2016-Feb-16 09:33:00':
                SymbolEntries.append(data)
    return SymbolEntries[-1:][0]


def handleScreenShotData():
    instrumentScreenShot = []
    for instrument in instruments:
        instrument["31"] = screenShot_31(instrument['Symbol'])
        instrument["32"] = screenShot_32(instrument['Symbol'])
        instrument["33"] = screenShot_33(instrument['Symbol'])
        instrumentScreenShot.append(instrument)
    return instrumentScreenShot


def calcArbitrage(buyCost):
    arbitrageOpptunbities = []
    stockPriceMap = {}
    S31 = (screenShot_31(510050)['Bid1']*screenShot_31(510050)['BidQty1']+screenShot_31(510050)['Ask1'] *
           screenShot_31(510050)['AskQty1'])/(screenShot_31(510050)['BidQty1']+screenShot_31(510050)['AskQty1'])
    S32 = (screenShot_32(510050)['Bid1']*screenShot_32(510050)['BidQty1']+screenShot_32(510050)['Ask1'] *
           screenShot_32(510050)['AskQty1'])/(screenShot_32(510050)['BidQty1']+screenShot_32(510050)['AskQty1'])
    S33 = (screenShot_33(510050)['Bid1']*screenShot_33(510050)['BidQty1']+screenShot_33(510050)['Ask1'] *
           screenShot_33(510050)['AskQty1'])/(screenShot_33(510050)['BidQty1']+screenShot_33(510050)['AskQty1'])
    stockPriceMap['31'] = S31
    stockPriceMap['32'] = S32
    stockPriceMap['32'] = S33

    screenShotData = handleScreenShotData()
    for d in stockPriceMap:
        for data in screenShotData:
            if data['Symbol'] != 510050:
                if (data['OptionType'] == 'C'):
                    if np.max(stockPriceMap[d]-data['Strike'], 0) > data[d]['Ask1'] + buyCost/10000:
                        arbitrageOpptunbities.append(
                            {
                                "optionType": data['OptionType'],
                                "symbol": data['Symbol'],
                                "Strike": data['Strike'],
                                "Ask": data[d]['Ask1'],
                                "size": data[d]['AskQty1'],
                                'time': data[d]['LocalTime']
                            }
                        )
                else:
                    if np.max(data['Strike']-stockPriceMap[d], 0) > data[d]['Ask1'] + buyCost/10000:
                        arbitrageOpptunbities.append(
                            {
                                "optionType": data['OptionType'],
                                "symbol": data['Symbol'],
                                "Strike": data['Strike'],
                                "Ask": data[d]['Ask1'],
                                "size": data[d]['AskQty1'],
                                'time': data[d]['LocalTime']
                            }
                        )

    print(arbitrageOpptunbities
          )


# By running calcArbitrage we can get arbitrage opptunities as below:
calcArbitrage(0)
# output:
# [{'optionType': 'C', 'symbol': 10000565, 'Strike': 1.8, 'Ask': 0.1554, 'size': 10.0, 'time': '2016-Feb-16 09:30:59.768077'}, {'optionType': 'C', 'symbol': 10000565, 'Strike': 1.8, 'Ask': 0.1575, 'size': 1.0, 'time': '2016-Feb-16 09:31:59.937279'}]

# output:
calcArbitrage(3.3)
# [{'optionType': 'C', 'symbol': 10000565, 'Strike': 1.8, 'Ask': 0.1554, 'size': 10.0, 'time': '2016-Feb-16 09:30:59.768077'}, {'optionType': 'C', 'symbol': 10000565, 'Strike': 1.8, 'Ask': 0.1575, 'size': 1.0, 'time': '2016-Feb-16 09:31:59.937279'}]
