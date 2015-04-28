import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
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

def main():
	
	testset = np.zeros((2,1000), dtype=float)
	tsx = np.arange(1000., dtype=float)
	#tsy = np.zeros_like(tsx)
	#tsy.fill(10.)
	tsy = np.sort(np.random.normal(500,0.1,1000))
	testset = np.array([tsx, tsy])
		
	#print('Test array x-vals 0-5:', testset[0,1:5])
	#print('Test array y-vals 0-5:', testset[1,1:5])
	
	test_tsp = trapezoidal_sp(testset)
	test_cumtrapz = integrate.cumtrapz(testset[1,:], testset[0,:], initial=0)
	test_trapz = integrate.trapz(testset[1,:], testset[0,:])
	n_test_cumtrapz = float(np.sum(test_cumtrapz))
	
	print('Function trapezoidal_sp yields:',test_tsp, '*')
	print('Function cumtrapz [-1] yields: ',test_cumtrapz[-1])
	print('Function trapz yields:         ',test_trapz)
	
	test_ssp = simpson_sp(testset)
	test_simps = integrate.simps(testset[1,:], testset[0,:])

	print('Function simpson_sp yields:    ',test_ssp, '*')
	print('Function simps yields:         ',test_simps)
	print('  Student Functions *')
	
	plt.close()                                             #closes hanging plotting data
	pdf_out = PdfPages('ex1_plots.pdf')                     #opens and initializes a PDF

	# Code for the first page of the PDF file above
	
	plt.figure(figsize=(8.27, 11.69), dpi = 200)            #initializes a A4 size page
	
	plt.subplot2grid((1,1), (0,0))                          #first of one graphs
	plt.plot(tsy, tsx, c='blue', lw=2)#plots the first line in blue
	plt.title('Test Curve Data %(num)d Points' % {"num":tsx.shape[0]})
	plt.xlabel('X Position')
	plt.ylabel('Y Value')
	
	plt.tight_layout()                                      #Fixes ovelapping text on page
	pdf_out.savefig()                                       #Prints to the first page
	pdf_out.close()                                         #closes opened pdf file





main()
	
	
