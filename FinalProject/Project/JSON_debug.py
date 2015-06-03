import requests as req
import simplejson
import sqlalchemy as sa
import time
import numpy as np
import scipy as sp
import copy
import csv as csv

def main(input_val):

  #
  # Begin preparation of constants and dynamic values to be used in code
  #

  #Declaring url lists for price history

  base_url = "https://cex.io/api/"
  
  last_price_url = base_url + "last_price/"  #JSON GET url...
  # {"curr1":"currency_1", "curr2":"currency_2", "lprice":"FLOAT"}
  
  price_stats_url= base_url + "price_stats/" # ....
  # price_stats: JSON POST {"lastHours":"INT", "maxRespArrSize": INT}
  # response:    list[..., {"tmsp":"unix_time", "price":"float"}, ...]
  
  ticker_url = base_url + "ticker/" #JSON GET url {"bid":"highest buy order",
  # "ask":"lowest sell order", "low":lowest price last 24h",
  # "high":"highest price last 24h", "last":"last price",
  # "volume":"volume of last 24h", "volume30d":"volume of last 30 days"}


  # Data structures for cryptocurrency name lists
  currency_dict = {"US Dollar":"USD", "Bitcoin":"BTC", "Litecoin":"LTC",
                   "Darkcoin":"DRK", "Dogecoin":"DOGE"}
  
  currency_pairs = ["BTC/USD/", "LTC/USD/", "LTC/BTC/", "DRK/BTC/", "DOGE/BTC/",
                    "DRK/LTC/", "DOGE/LTC/"]

  
  # Generate lists of URLs to request data from from using JSON
  price_stats_url_list = []
  for item in currency_pairs:
    price_stats_url_list.append(price_stats_url + item)
 
  last_price_url_list = []
  for item in currency_pairs:
    last_price_url_list.append(last_price_url + item)
  
  ticker_url_list = []
  for item in currency_pairs:
    ticker_url_list.append(ticker_url + item)  
 
 
  #declaration of timing variables 
  current_time = time.time()  

  unix_week = int(604800) #number of seconds in a week
  unix_season = int(7884000) #number of seconds in a season of 91d 6h
  
  previous_week_start = int(current_time - unix_week)
  previous_season_start = int(current_time - unix_season)

  week_hours = int(168)
  season_hours = int(2190)
  
  cex_start_time = 1372636800 #0:00 July 1st 2013 in Unix time code
  cex_uptime = int(current_time - cex_start_time)
  cex_hours = np.ceil(cex_uptime/3600)


  #
  # Begin JSON pulling and writing to CSV file code
  #
  
  external_json_response = []
  
  for working_url in price_stats_url_list:
    
    #prepare payload and header data
    payload = {"lastHours":100, "maxRespArrSize":unix_week}
    header = {"content-type": "application/x-www-form-urlencoded", "User-agent": "bot-cex.io"}
    body_payload = {"lastHours": "24", "maxRespArrSize": "1000"}
    
    #attempt to post data packet to appropriate URL and get response
    #try:
      #response = req.post(working_url, data=simplejson.dumps(payload),
      #                    headers=headers)
    response = req.request('POST',working_url, data=body_payload, headers=header)
    #except Exception as exc:
     # print("Exception as: " + str(exc))
    
    #Unpack the JSON formatted response
    json_data = response.json()
    
    external_json_response = copy.copy(json_data)
    
    f_name = 'day_3_'
    #First part of file name generator 
    if(working_url[-8] == "/"):
      f_name = f_name + working_url[-7:]
      f_name = f_name.replace("/", "_")
    elif(working_url[-9] == "/"):
      f_name = f_name + working_url[-8:]
      f_name = f_name.replace("/", "_")
    else:
      f_name = f_name + working_url[-9:]
      f_name = f_name.replace("/", "_")
    #Second part of file name generator  
    if("last_price" in working_url):
      f_name = f_name + "last_price"
    elif("price_stats" in working_url):
      f_name = f_name + "price_stats"
    elif("ticker" in working_url):
      f_name = f_name + "ticker"
    else:
      f_name = f_name 
      
    field_names = ['price', 'tmsp']
    
    with open("%(f_name)s.csv" % {"f_name": f_name},'w',newline='') as csv_out:
      csvwriter = csv.DictWriter(csv_out, delimiter=',',fieldnames=field_names,
                                 quoting=csv.QUOTE_NONNUMERIC)
      csvwriter.writeheader()
      csvwriter.writerows(json_data)
    
    
      
  
  
  
  #
  # Begin plotting of data phase
  #


  print("break")

if __name__ == "__main__":
  input_val = 0
  main(input_val)