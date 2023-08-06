import pandas as pd
from QiDataLoader.MqDataLoader import MqDataLoader
import datetime
from QiDataLoader.EnumBarType import EnumBarType
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.width',1000)

barType = EnumBarType.Day
instrumentIdA = "IF1812"
instrumentIdB = "IF1901"
beginDate = datetime.date(2018, 12, 12)
endDate = datetime.date(2018, 12, 30)
dataLoader = MqDataLoader("//192.168.1.200/MqData/futuretick/Future")
minPath = "//192.168.1.200/MqData/futuremin"
dayPath = "//192.168.1.200/MqData/futureday"

if barType == EnumBarType.Minute:
    barSeries = dataLoader.GetMinBarSeries(instrumentIdA, beginDate, endDate, minPath)
    lstA = []
    for bar in barSeries:
        lstA.append([bar.TradingDate, bar.BeginTime, bar.EndTime, bar.Open, bar.High, bar.Low, bar.Close, bar.PreClose, bar.Volume])
    dfA = pd.DataFrame(lstA, columns=['TradingDate', 'BeginTime', 'EndTime', 'Open', 'High', 'Low', 'Close', 'PreClose', 'Volume'])

    print(dfA)
elif barType == EnumBarType.Day:
    barSeries = dataLoader.GetDayBarSeries(instrumentIdA, beginDate, endDate, dayPath)
    lstA = []
    for bar in barSeries:
        lstA.append([bar.TradingDate, bar.High, bar.Open, bar.Low, bar.Close, bar.Volume, bar.Turnover, bar.OpenInterest])
    dfA = pd.DataFrame(lstA, columns=['TradingDate', 'High', 'Open', 'Low', 'Close', 'Volume', 'Turnover', 'OpenInterest'])

    print(dfA)
else:
    tickSeriesA = dataLoader.GetTickSeries(instrumentIdA, beginDate, endDate)
    lstA = []
    for tick in tickSeriesA:
        lstA.append([tick.DateTime, tick.LastPrice, tick.AskPrice1, tick.BidPrice1, tick.AskVolume1, tick.BidVolume1])
    dfA = pd.DataFrame(lstA, columns=['DateTime', 'LastPrice', 'AskPrice1', 'BidPrice1', 'AskVolume1', 'BidVolume1'])

    print(dfA)