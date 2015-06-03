import requests as req
import simplejson
import sqlalchemy as sa
import time
import numpy as np
import scipy as sp
import copy
import csv as csv
from operator import itemgetter


def main(input_val):
    currency_pairs = ["BTC_USD_", "LTC_USD_", "LTC_BTC_", "DRK_BTC_",
                      "DOGE_BTC_", "DRK_LTC_", "DOGE_LTC_"]
    
    file_list = []
    file_list_uber = []
    
    for pair in currency_pairs:
        file_list.append(pair + "full.csv")
    
    #
    #  Ubersample data and write to numpy array for filled every second data
    #
    
    for file in file_list:
        full_csv = open(file, 'r')
        csv_read = csv.DictReader(full_csv, delimiter=',',
                                  quoting=csv.QUOTE_NONNUMERIC)
        csv_list = []
        for row in csv_read:
            csv_list.append({'price':float(row['price']),
                             'tmsp':int(row['tmsp'])})            
            
        first_tmsp = int(csv_list[0]['tmsp'])
        last_tmsp = int(csv_list[-1]['tmsp'])
        uber_len = int((last_tmsp - first_tmsp)/100) + 1
        
        uber_tmsp_array = np.arange(first_tmsp, last_tmsp+100, 100, dtype=int)
        
        uber_price_array = np.zeros(len(uber_tmsp_array), dtype='float')
        uber_price_array[0] = csv_list[0]['price']        
        uber_index = 0
        
        max_tmsp_sep_100s = 0
        min_tmsp_sep_100s = uber_len
        
        #populate ubersampled price array using linear interpolation
        for i in range(0,len(csv_list)-1, 1):
            tmsp_1 = int(csv_list[i]['tmsp'])
            tmsp_2 = int(csv_list[i+1]['tmsp'])
            tmsp_delta = int((tmsp_2 - tmsp_1)/100)
            
            price_1 = csv_list[i]['price']
            price_2 = csv_list[i+1]['price']
            price_delta = price_2 - price_1
            price_step = price_delta / tmsp_delta
            
            #compute accessory data for filtering FFT of ubersampled data later
            if tmsp_delta > max_tmsp_sep_100s:
                max_tmsp_sep_100s = tmsp_delta
            elif tmsp_delta < min_tmsp_sep_100s:
                min_tmsp_sep_100s = tmsp_delta
                
            #Start filling price array with ubersampled data
            for j in range(1,tmsp_delta,1):
                uber_index = uber_index + 1
                uber_price_array[uber_index] = price_1 + (j * price_step)
                
                #use known value of price_2 at i+1 for the last iteration
            uber_index = uber_index + 1
            uber_price_array[uber_index] = price_2
            
            
        full_csv.close()
        
        field_names = ['price', 'tmsp']
        uber_csv_name = file[0:-4] + "_ubersampled.csv"
        file_list_uber.append(uber_csv_name)
        uber_csv = open(uber_csv_name, 'w', newline = '')
        
        csvwriter = csv.DictWriter(uber_csv, delimiter=',',fieldnames=field_names,
                                   quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writeheader()
        #csvwriter.writerows(full_conditioned)
        
        for i in range(0,len(uber_tmsp_array),1):
            dict_d = {'tmsp':uber_tmsp_array[i], 'price':uber_price_array[i]}
            csvwriter.writerow(dict_d)
            
        uber_csv.close()
        
        
        
if __name__ == "__main__":
    input_val = 0
    main(input_val)                    