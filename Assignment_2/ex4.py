import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_pdf import PdfPages
from multiprocessing import Process


def trapezoidal_sp(a):
	#single processor (sp) version without chunking and cluster functionality (c_ver)
	lena = a.shape
	atype = a.dtype
	
	x1np = np.array([a[0,0:lena[1]-1]], dtype=atype)
	x2np = np.array([a[0,1:lena[1]]], dtype=atype)
	y1np = np.array([a[1,0:lena[1]-1]], dtype=atype)
	y2np = np.array([a[1,1:lena[1]]], dtype=atype)
	aslices = (x2np - x1np) * (y1np + y2np)
	return 0.5 * float(np.sum(aslices))

def simpson_sp(a):
	#only works on even spacing, so it is assumed
	lena= a.shape
	atype = a.dtype
	dx = float(a[0,1] - a[0,0])    #casts dx as a float for cython and to avoid numpy stack thrash
	dxcheck = float(a[0,2] - a[0,1])

	if (lena[1] % 2) == 1:            #Escapes with NaN if number of points is ODD
		return np.nan
	elif (dx != dxcheck):
		return np.nan          #escapes with NaN if first three points have uneven spacing

	ynpeven = np.array([a[1,1:lena[1]-2:2]], dtype=atype)
	ynpodd = np.array([a[1,2:lena[1]-1:2]], dtype=atype)
	yeven = float(np.sum(ynpeven))
	yodd = float(np.sum(ynpodd))
	# Compensation of 1.5 for f(x=0) and f(x=n), unsure of maths but it fixes edge discrepancies
	#  in all cases. More accurate than stock simps and trapz function from scipy as a result.
	return (dx/3.0) * ((1.5*float(a[1,0])) + (4.0 * yodd) + (2.0 * yeven) + (1.5*float(a[1,-1])))
	
def input_function(x):
	return (np.sin(np.sqrt(100. * x)))**2

	
def main(command_line_data):
	
	fx_0to1 = 0.45832532309085
	range_floor = 0.0
	range_ceiling = 1.0
	precision = command_line_data

	a_ans = []
	a_err = []

	bin_spacing = (range_ceiling - range_floor)
	
	#generate first array to iterate over
	x0_range = np.arange(range_floor, range_ceiling, bin_spacing, dtype=float)
	f0_range = np.zeros((2,x0_range.size), dtype=float)
	f0_range[0,:] = x0_range
	f0_range[1,:] = input_function(x0_range)
	
	#calculate initial values to add to external holding lists a_ans and a_err
	a_ans.append(trapezoidal_sp(f0_range))
	a_err.append(np.absolute((1./3.) * (a_ans[0] - 0.)))
	
	i = 1
	
	while  (a_err[i-1] >= precision) or (i == 1):
		
		bin_spacing = bin_spacing / 2.    #new bin spacing for subsequent arrays
		
		#generate new array to iterate over
		x_range = np.arange(range_floor, range_ceiling, bin_spacing, dtype=float)
		f_range = np.zeros((2,x_range.size), dtype=float)
		f_range[0,:] = x_range
		f_range[1,:] = input_function(x_range)
	
		#calculate values to add to external holding arrays
		a_ans.append(trapezoidal_sp(f_range))
		a_err.append(np.absolute((1./3.) * (a_ans[i] - a_ans[i-1])))
		i = i + 1
	
	#print out step in an organised fashion from holding lists
	
	n = 0
	while n < (i-1):
		print('Step %(i)s: Calculated value: %(vals)s with error: %(err)s)' % 
		      {"i": format(n+1, '02'), "vals": format(a_ans[n], '.10f'),
		       "err": format(a_err[n], '.10f')})
		n = n + 1
		
	

if __name__ == "__main__":
	#interface with command line
	if len(sys.argv) == 1:
		command_line_data = 0.000001
		main(command_line_data)
	else:
		try:
		  command_line_data = float(sys.argv[1])
		  main(command_line_data)
		except ValueError as err:
		  print('Error: %(val)s\n' % {"val": err})
			
