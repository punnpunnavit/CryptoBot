from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from datetime import datetime
import talib
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv('FIRST_SECRET'), os.getenv('SECOND_SECRET'))

def current_date_time():
 now = datetime.now()
 dt_string = now.strftime("Date:%d/%m/%Y Time:%H:%M:%S")
 return dt_string

def get_coin_data(coin,custom_frequency = Client.KLINE_INTERVAL_1DAY,custom_start='1 Jan 2021'):
    close_arr,open_arr,high_arr,low_arr,vol_arr,date_arr= ([] for i in range(6))
    data = client.get_historical_klines(coin, custom_frequency ,custom_start)
    for i in data:
       open_arr.append(float(i[1]))
       high_arr.append(float(i[2]))
       low_arr.append(float(i[3]))
       close_arr.append(float(i[4]))
       vol_arr.append(float(i[5]))
       date_arr.append( datetime.fromtimestamp(int(i[6]/1000)))
    sum_arr = [open_arr,close_arr,high_arr,low_arr,vol_arr,date_arr]
    np_data = np.array(sum_arr)
    return np_data

# get_coin_data('BNBUSDT',Client.KLINE_INTERVAL_1DAY)

def get_graph(indicator_val,indicator_name,val,coin,date):
  plt.plot(date,indicator_val,label=indicator_name, linestyle='--')
  plt.plot(date,val,label=coin)
  plt.legend(loc="best")
  plt.show()

def get_single_graph(indicator_val,indicator_name,date):
  plt.plot(date,indicator_val,label=indicator_name, linestyle='--')
  plt.legend(loc="best")
  plt.show()

def get_current_price(coin):
  price = get_coin_data(coin,Client.KLINE_INTERVAL_1MINUTE,"1 minute ago")
  current_price = ((float)(price[0][0]) + (float)(price[1][0]) + (float)(price[2][0]) + (float)(price[3][0]))/4
  print(coin + " : " ,"{:.2f}".format(current_price))

#trend indicator
def EMA(coin,interval):
  data = get_coin_data(coin)
  close_data = [float(x) for x in data[1]]
  for i in close_data:
    print(type(i))
  real = talib.EMA(np.array(close_data), timeperiod=interval)
  get_graph(real,"EMA" + str(interval),close_data,coin,data[5])

#momentum indicator good for long trade
def ADX(coin,interval):
    data = get_coin_data(coin)
    close_data = [float(x) for x in data[1]]
    low_data = [float(x) for x in data[3]]
    high_data = [float(x) for x in data[2]]

    real = talib.ADX(np.array(high_data), np.array(low_data), np.array(close_data), timeperiod=interval)
    get_single_graph(real,"ADX",data[5])

def SAR():
  real = SAR(high, low, acceleration=0.02, maximum=0.20)


# indicators

#trend => lagging EMA5 50 200(บอกค่าเฉลี่ยโดยweigh ไม่เท่า),
  #lagging ADX(Average Directional Movement Index) เปรียบเทียบความแข็งแกร่งขึ้นและลง คำนวณจาก DI+ บอกความแข่งแกร่งของbullish by comparing each day High,Low CLose,DI-บอกความแข็งแกร่งของbearish,
  #leading Parabolic Stop and Reverse (SAR) แม่นมากใน uptrend and downtrend บอกว่าราคาจะขึ้นหรือลงแล้วแรงขนาดไหน ไข่ปลาบนลง ไข่ปลาล่างขึ้น ห่างแรง,
  #Fibonacci Retracement leading

#volume(Strength) => ADL เพื่อที่จะทำการยืนยันเทรนด์ปัจจุบัน หรือทำนายการกลับตัวในอนาคต,The A/D line helps to show how supply and demand factors are influencing price, is a cumulative indicator that uses volume and price to assess whether a stock is being accumulated or distributed., A/D=Previous A/D+((Close-low)+(high-close)/(high-low))*period volume

#OBV, บอกว่ามีนักลงทุนเข้าใหม่ หรือออกไปมากน้อยเพียวน้อยเพียงใด ถ้าราคาปิดวันนี้ > วันก่อน  =>  OBVใหม่ = OBVเดิม+ปริมาณหุ้นวันนี้ ถ้าราคาปิดวันนี้ < วันก่อน => OBVใหม่ = OBVเดิม-ปริมาณหุ้นวันนี้ ถ้าราคาปิดวันนี้ =วั นก่อน => OBVใหม่ = OBVเดิม
#volume rate of change(VROC), [ (ปริมาณซื้อขายปัจจุบัน / ปริมาณซื้อขาย ณ วันที่ผ่านมาแล้ว (n-วัน) ) -1 ] * 100 ค่า VROC เพิ่มขึ้น = ปริมาณการซื้อขาย ณ วันปัจจุบันเพิ่มขึ้นมากกว่าปริมาณการซื้อขายในช่วงระยะเวลา n วัน ค่า VROC ลดลง = ปริมาณการซื้อขาย ณ วันปัจจุบัน น้อยกว่าปริมาณการซื้อขายในช่วงระยะเวลา n วัน

#Average Directional Movement Index

#momentum =>  RSI , RSI อยู่ในระดับที่ตํ่ากว่า 30 จะถือว่าราคาอยู่ในภาวะ “ขายมากเกินไป” (Oversold) และหากมากกว่า 70 จะถือว่าราคาอยู่ในภาวะ “ซื้อมากเกินไป” ซื้อมากเกินจนแพงจนไม่มีคนซื้อ (Overbought)
#Stochastic(MACD+RSI) เหมาะสำหรับระยะสั้น, %K close-low/high/low * 100 %D avg of K% %K > 80 overbought %K<20 oversold เมื่อ %K ตัดขึ้นเหนือ % D (ค่าเฉลี่ยของตัวเอง) ขึ้นไป และเกิดขึ้นที่ Oversold อาจเป็นสัญญาณซื้อ เมื่อ %K ตัดลงมาต่ำกว่า % D (ค่าเฉลี่ยของตัวเอง) และเกิดขึ้นที่ Overbought อาจเป็นสัญญาณขาย
#MACD(EMA12,Zero line,EMA26) ,
#CCI,
#Ichimoku Cloud

#volatility => 
#ATR ,
#Standard deviation,
#bollinger band
