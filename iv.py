from scipy.special import y0_zeros
import numpy as np
from scipy.stats import norm
import pandas as pd
import csv
import matplotlib.pyplot as plt


N = norm.cdf
N_prime = norm.pdf


def BS_CALL_CALL(S, K, T, sigma, r, q):
    d1 = (np.log(S/K) + (r-q)*(T)) / \
        (sigma*np.sqrt(T)) + (sigma/2)*np.sqrt(T)
    d2 = d1 - sigma * np.sqrt(T)
    callPrice = S*np.exp(-q*(T)) * N(d1) - K * np.exp(-r*(T)) * N(d2)
    return callPrice


def BS_CALL_PUT(S, K,  T, sigma, r, q):
    d1 = (np.log(S/K) + (r-q)*(T)) / \
        (sigma*np.sqrt(T)) + (sigma/2)*np.sqrt(T)
    d2 = d1 - sigma * np.sqrt(T)
    putPrice = K*np.exp(-r*(T))*N(-d2) - S*np.exp(-q*(T))*N(-d1)

    return putPrice


def vega(S, K, T, sigma, r, q):
    d1 = (np.log(S/K) + (r-q)*(T)) / \
        (sigma*np.sqrt(T)) + (sigma/2)*np.sqrt(T)
    vega = S * N_prime(d1) * np.sqrt(T)
    return vega


def IMPLIED_VOLATILITY_CALL(C, S, K, T, r, q):
    sigmahat = np.sqrt(2*abs((np.log(S/K) + (r-q)*(T))/(T)))
    tol = 1e-8
    nmax = 100
    sigmadiff = 1
    n = 1
    sigma = sigmahat
    while (sigmadiff >= tol and n < nmax):
        Cvega = vega(S, K, T, sigma, r, q)
        increment = (BS_CALL_CALL(S, K, T, sigma, r, q)-C)/Cvega
        sigma = sigma - increment
        n = n+1
        sigmadiff = abs(increment)
    return sigma


def IMPLIED_VOLATILITY_PUT(P, S, K, T, r, q):
    sigmahat = np.sqrt(2*abs((np.log(S/K) + (r-q)*(T))/(T)))
    tol = 1e-8
    nmax = 100
    sigmadiff = 1
    n = 1
    sigma = sigmahat
    while (sigmadiff >= tol and n < nmax):
        Pvega = vega(S, K, T, sigma, r, q)
        increment = (BS_CALL_CALL(S, K, T, sigma, r, q)-P)/Pvega
        sigma = sigma - increment
        n = n+1
        sigmadiff = abs(increment)
    return sigma


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


vol31ByKey = {}
vol32ByKey = {}
vol33ByKey = {}


def calVol():
    T = (24-16)/365
    r = 0.04
    q = 0.2
    S31 = (screenShot_31(510050)['Bid1']*screenShot_31(510050)['BidQty1']+screenShot_31(510050)['Ask1'] *
           screenShot_31(510050)['AskQty1'])/(screenShot_31(510050)['BidQty1']+screenShot_31(510050)['AskQty1'])
    S32 = (screenShot_32(510050)['Bid1']*screenShot_32(510050)['BidQty1']+screenShot_32(510050)['Ask1'] *
           screenShot_32(510050)['AskQty1'])/(screenShot_32(510050)['BidQty1']+screenShot_32(510050)['AskQty1'])
    S33 = (screenShot_33(510050)['Bid1']*screenShot_33(510050)['BidQty1']+screenShot_33(510050)['Ask1'] *
           screenShot_33(510050)['AskQty1'])/(screenShot_33(510050)['BidQty1']+screenShot_33(510050)['AskQty1'])

    screenShotData = handleScreenShotData()
    for data in screenShotData:
        if data['Symbol'] != 510050:
            voldata31 = {}
            voldata32 = {}
            voldata33 = {}
            strike_value = data["Strike"]

            if strike_value in vol31ByKey:
                voldata31 = vol31ByKey[strike_value]
            if strike_value in vol32ByKey:
                voldata32 = vol32ByKey[strike_value]
            if strike_value in vol33ByKey:
                voldata33 = vol33ByKey[strike_value]
            if data['OptionType'] == "P":
                voldata31['BidVolP'] = IMPLIED_VOLATILITY_PUT(
                    data['31']['Bid1'], S31,  data['Strike'], T, r, q)
                voldata31['AskVolP'] = IMPLIED_VOLATILITY_CALL(
                    data['31']['Ask1'], S31, data['Strike'], T, r, q)
                voldata32['BidVolP'] = IMPLIED_VOLATILITY_PUT(
                    data['32']['Bid1'], S32,  data['Strike'], T, r, q)
                voldata32['AskVolP'] = IMPLIED_VOLATILITY_CALL(
                    data['32']['Ask1'], S32, data['Strike'], T, r, q)
                voldata33['BidVolP'] = IMPLIED_VOLATILITY_PUT(
                    data['33']['Bid1'], S33,  data['Strike'], T, r, q)
                voldata33['AskVolP'] = IMPLIED_VOLATILITY_CALL(
                    data['33']['Ask1'], S33, data['Strike'], T, r, q)
            else:
                voldata31['BidVolC'] = IMPLIED_VOLATILITY_PUT(
                    data['31']['Bid1'], S31,  data['Strike'], T, r, q)
                voldata31['AskVolC'] = IMPLIED_VOLATILITY_CALL(
                    data['31']['Ask1'], S31, data['Strike'], T, r, q)
                voldata32['BidVolC'] = IMPLIED_VOLATILITY_PUT(
                    data['32']['Bid1'], S32,  data['Strike'], T, r, q)
                voldata32['AskVolC'] = IMPLIED_VOLATILITY_CALL(
                    data['32']['Ask1'], S32, data['Strike'], T, r, q)
                voldata33['BidVolC'] = IMPLIED_VOLATILITY_PUT(
                    data['33']['Bid1'], S33,  data['Strike'], T, r, q)
                voldata33['AskVolC'] = IMPLIED_VOLATILITY_CALL(
                    data['33']['Ask1'], S33, data['Strike'], T, r, q)
        vol31ByKey[strike_value] = voldata31
        vol32ByKey[strike_value] = voldata32
        vol33ByKey[strike_value] = voldata33


calVol()


def transformArray(hashMap):
    array = []
    for d in iter(hashMap):
        obj = hashMap[d]
        obj['Strike'] = d
        array.append(hashMap[d])
    return array


vol31 = transformArray(vol31ByKey)
vol32 = transformArray(vol32ByKey)
vol33 = transformArray(vol33ByKey)
# output data to csv files
# fields = ['Strike', 'BidVolC', 'AskVolC', 'BidVolP', 'AskVolP']
# with open('31.csv', 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=fields)
#     writer.writeheader()
#     writer.writerows(vol31)

# with open('32.csv', 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=fields)
#     writer.writeheader()
#     writer.writerows(vol32)
# with open('33.csv', 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=fields)
#     writer.writeheader()
#     writer.writerows(vol33)


def smoothNan(vol, key):
    x = []
    y = []
    i = 0
    while i < len(vol) - 1:
        if vol[i][key] != 'nan':
            x.append(vol[i]['Strike'])
            y.append(vol[i][key])
    return {
        'x': x,
        'y': y
    }

# print Plot


def plot(vol):
    plt.plot(smoothNan(vol, "BidVolC")['x'], smoothNan(
        vol, "BidVolC")['y'], label="BidVolC", linestyle='-')
    plt.plot(smoothNan(vol, "BidVolP")['x'], smoothNan(
        vol, "BidVolP")['y'], label="BidVolP", linestyle='-')
    plt.plot(smoothNan(vol, "AskVolC")['x'], smoothNan(
        vol, "AskVolC")['y'], label="BidVolP", linestyle='-')
    plt.plot(smoothNan(vol, "AskVolP")['x'], smoothNan(
        vol, "AskVolP")['y'], label="BidVolP", linestyle='-')
    plt.legend()
    plt.show()


plot(vol31)
plot(vol32)
plot(vol33)
