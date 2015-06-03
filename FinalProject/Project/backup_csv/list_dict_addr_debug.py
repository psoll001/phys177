
def main():
    
    list_csv = [{'tmsp':10000., 'price': 100.},
                {'tmsp':10001., 'price': 101.},
                {'tmsp':10002., 'price': 102.},
                {'tmsp':10003., 'price': 103.},
                {'tmsp':10004., 'price': 104.},
                {'tmsp':10005., 'price': 105.},
                {'tmsp':10006., 'price': 106.},
                {'tmsp':10007., 'price': 107.},
                {'tmsp':10008., 'price': 108.},
                {'tmsp':10009., 'price': 109.}]
    
    d_0_tmsp = list_csv[0]['tmsp']
    d_0_price = list_csv[0]['price']
    
    d_5_tmsp = int(list_csv[5]['tmsp'])
    d_9_price = list_csv[-1]['price']
    
    for i in range(1,2,1):
        d_9_price = d_9_price + 1.
    
    print('break')
    print('break2')
    
main()