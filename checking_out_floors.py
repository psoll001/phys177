import math
import numpy as np
import time

def fools(ary):
	bry = ary//3
	return bry

def foolz(ary):
	bry = (ary//3) +1
	return bry
x = 49
xf = 49.0

y = x/5
yf = x/5.0

z = x//5
zf = x//5.0

print ('x=', x, 'xf=', xf)
print ('y=', y, 'yf=', yf)
print ('z=', z, 'zf=', zf)

ma = x/5.0
mb = xf/5

na = x//5.0
nb = xf//5

print ('ma=', ma, 'mb=', mb)
print ('na=', na, 'nb=', nb)

a = np.arange(1.0,10.0)
print(a)
b = a//3.0
print(b)
b = a//3
print(b)

c = fools(a)
print('function test:', c)

a = np.arange(1,10)
print(a)
b = a//3
print(b)
b = a//3.0
print(b)

c = fools(a)
print('function test:', c)

big_a = np.arange(1,10,2)
big_b = np.zeros_like(big_a)

it_i = 0                                                              #external indexer
t0 = time.clock()                                                     #start timer for loop
	
#for x in np.nditer(big_a, flags=['external_loop']):
for x in np.nditer(big_a):
	print ('value:', 'big_a[x]','index:', x)
	#big_b[x] = foolz(big_a[x])
	
t1 = time.clock() - t0                                       #calculate time for loop to run
print('Calculated in', t1, 'seconds with exteral looping.')           #print results
it_i = 0                 

