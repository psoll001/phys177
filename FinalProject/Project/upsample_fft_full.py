import requests as req
import simplejson
import sqlalchemy as sa
import time
import numpy as np
from numpy import fft
import scipy as sp
import copy
import csv as csv
from operator import itemgetter


def main(input_val):
    currency_pairs = ["BTC_USD_", "LTC_USD_", "LTC_BTC_", "DRK_BTC_",
                      "DOGE_BTC_", "DRK_LTC_", "DOGE_LTC_"]
    
    file_list_uber = []
    
    for pair in currency_pairs:
        file_list_uber.append(pair + "full_ubersampled.csv")
    
    for file in file_list_uber:
        uber_csv = open(file, 'r')
        csv_read = csv.DictReader(uber_csv, delimiter=',',
                                  quoting=csv.QUOTE_NONNUMERIC)
        csv_list = []
        for row in csv_read:
            csv_list.append({'price':float(row['price']),
                             'tmsp':int(row['tmsp'])})            
                    
        first_tmsp = int(csv_list[0]['tmsp'])
        last_tmsp = int(csv_list[-1]['tmsp'])
        delta_tmsp = int(last_tmsp - first_tmsp)
            
        uber_len = len(csv_list)
            
        uber_price_array = np.zeros(uber_len, dtype='float')
            
        for i in range(0,uber_len,1):
            uber_price_array[i] = csv_list[i]['price']
            
        uber_fft = fft.rfft(uber_price_array)
        uber_fft_imag = np.imag(uber_fft)
        uber_fft_real = np.real(uber_fft)
        uber_fft_mag = np.sqrt((uber_fft_real * uber_fft_real) +
                               (uber_fft_imag * uber_fft_imag))
        
        uber_fft_bins = fft.rfftfreq(uber_len, d=100)
        
        uber_csv.close()
                
        field_names = ['freq_bin', 'magnitude']
        fft_csv_name = file[0:-4] + "_fft.csv"
        
        fft_csv = open(fft_csv_name, 'w', newline = '')
                
        csvwriter = csv.DictWriter(fft_csv, delimiter=',',fieldnames=field_names,
                                   quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writeheader()
        #csvwriter.writerows(full_conditioned)
                
        for i in range(0,len(uber_fft_real),1):
            dict_d = {'freq_bin':uber_fft_bins[i],
                      'magnitude':uber_fft_mag[i]}
            csvwriter.writerow(dict_d)
                    
        fft_csv.close()        
        
        
               
if __name__ == "__main__":
    input_val = 0
    main(input_val)       