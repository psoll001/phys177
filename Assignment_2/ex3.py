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
	return (dx/3.0) * ((1.5*float(a[1,0])) + (4.0 * yodd) + (2.0 * yeven) + (1.5*float(a[1,-1])))
	
def input_function(x):
	return (x * x * x * x) - (2.0 * x) + 1.0
	
def input_function_prime(x):
	return (4.0 * x * x * x) - (2.0)

def trapezoidal_error(n, a, b):
	return (0 - ((b-a)**2 / (12.*n*n))) * (input_function_prime(b) - input_function_prime(a))

	
def main(command_line_data):
	
	fx_0to2 = 4.40
	range_floor = 0.0
	range_ceiling = 2.0
	bin_spacing = (range_ceiling - range_floor) / command_line_data
	
	
	#x2_range = np.arange(range_floor, range_ceiling, bin_spacing/2, dtype=float)	
	x1_range = np.arange(range_floor, range_ceiling, bin_spacing, dtype=float)
	x0_range = np.arange(range_floor, range_ceiling, bin_spacing*2, dtype=float)

	#f2_range = np.zeros((2,x2_range.size), dtype=float)
	f1_range = np.zeros((2,x1_range.size), dtype=float)
	f0_range = np.zeros((2,x0_range.size), dtype=float)
	
	#f2_range[0,:] = x2_range
	#f2_range[1,:] = input_function(x2_range)
	
	f1_range[0,:] = x1_range
	f1_range[1,:] = input_function(x1_range)
	
	f0_range[0,:] = x0_range
	f0_range[1,:] = input_function(x0_range)
	
	#trapezoidal_sp2_out = trapezoidal_sp(f2_range)
	trapezoidal_sp1_out = trapezoidal_sp(f1_range)
	trapezoidal_sp0_out = trapezoidal_sp(f0_range)

	#simpson_sp2_out = simpson_sp(f2_range)
	simpson_sp1_out = simpson_sp(f1_range)
	simpson_sp0_out = simpson_sp(f0_range)

	#trapz2_out = integrate.trapz(f2_range[1,:], f2_range[0,:])	
	trapz1_out = integrate.trapz(f1_range[1,:], f1_range[0,:])
	trapz0_out = integrate.trapz(f0_range[1,:], f0_range[0,:])

	#simps2_out = integrate.simps(f2_range[1,:], f2_range[0,:])
	simps1_out = integrate.simps(f1_range[1,:], f1_range[0,:])
	simps0_out = integrate.simps(f0_range[1,:], f0_range[0,:])
	
	trapezoidal_sp1_err = (1./3.) * (trapezoidal_sp1_out - trapezoidal_sp0_out)
	simpson_sp1_err = (1./15.) * (simpson_sp1_out - simpson_sp0_out)
	trapz1_err = (1./3.) * (trapz1_out - trapz0_out)
	simps1_err = (1./15.) * (simps1_out - simps0_out)

	'''
	trapezoidal_sp2_err = (1./3.) * (trapezoidal_sp2_out - trapezoidal_sp1_out)
	simpson_sp2_err = (1./15.) * (simpson_sp2_out - simpson_sp1_out)
	trapz2_err = (1./3.) * (trapz2_out - trapz1_out)
	simps2_err = (1./15.) * (simps2_out - simps1_out)
	'''
	
	print('Integration of f(x) = (x^4 - 2x + 1) from x=0 to x=2 yields the following...','\n')
	print('Trapezoidal_sp funtion using %(bins)d slices: %(ans)s' %
	      {"bins": command_line_data, "ans": format(trapezoidal_sp1_out, '.10f')})
	print('Simpson_sp function    using %(bins)d slices: %(ans)s' %
	      {"bins": command_line_data, "ans": format(simpson_sp1_out, '.10f')})
	print('Scipy\'s trapz funtion  using %(bins)d slices: %(ans)s' % 
	      {"bins": command_line_data, "ans": format(trapz1_out, '.10f')})
	print('Scipy\'s simps function using %(bins)d slices: %(ans)s' % 
	      {"bins": command_line_data, "ans": format(simps1_out, '.10f')}, '\n')
	
	print('Real value is:', format(fx_0to2, '.10f'),'\n')

	print('Error estimation for trapezoidal_sp funtion using %(bins)d slices: %(ans)s' %
	      {"bins": command_line_data, "ans": format(trapezoidal_sp1_err, '.10f')})
	print('Error estimation for simpson_sp function    using %(bins)d slices: %(ans)s' %
	      {"bins": command_line_data, "ans": format(simpson_sp1_err, '.10f')})
	print('Error estimation for Scipy\'s trapz funtion  using %(bins)d slices: %(ans)s' % 
	      {"bins": command_line_data, "ans": format(trapz1_err, '.10f')})
	print('Error estimation for Scipy\'s simps function using %(bins)d slices: %(ans)s' % 
	      {"bins": command_line_data, "ans": format(simps1_err, '.10f')}, '\n')

	print('Real error for trapezoidal_sp funtion using %(bins)d slices: %(ans)s' %
	      {"bins": command_line_data, "ans": format((fx_0to2-trapezoidal_sp1_out), '.10f')})
	print('Real error for simpson_sp function    using %(bins)d slices: %(ans)s' %
	      {"bins": command_line_data, "ans": format((fx_0to2-simpson_sp1_out), '.10f')})
	print('Real error for Scipy\'s trapz funtion  using %(bins)d slices: %(ans)s' % 
	      {"bins": command_line_data, "ans": format((fx_0to2-trapz1_out), '.10f')})
	print('Real error for Scipy\'s simps function using %(bins)d slices: %(ans)s' % 
	      {"bins": command_line_data, "ans": format((fx_0to2-simps1_out), '.10f')}, '\n')
	
	

if __name__ == "__main__":
	#interface with command line
	if len(sys.argv) == 1:
		command_line_data = 20
		main(command_line_data)
	else:
		try:
		  command_line_data = int(sys.argv[1])
		  main(command_line_data)
		except ValueError as err:
		  print('Error: %(val)s\n' % {"val": err})
			
