import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math

def final_grade(homework, midterm, final_project):
	return (homework * 0.40) + (midterm * 0.20) + (final_project * 0.40)

def main():
	
	homework_weight = 0.40
	midterm_weight = 0.20
	final_project_weight = 0.40

	homework_grades = np.array([10.,10.,8.,9.5,3.,9.,0.,6.], dtype=float)
	midterm_grades = np.array([10.,10.,10.,10.,8.,5.,10.,7.])
	final_project_grades = np.array([9.,10.,10.,6.,10.,6.,8.,9.])
	
	final_grades = np.zeros_like(homework_grades)
	final_grades = final_grade(homework=homework_grades, midterm=midterm_grades,
                                   final_project=final_project_grades)	
	
	
	#begin program output phase
	
	fail_list = []
	ap_list = []
	
	txt_out = open('ex2.txt','w')                          #initialize text file for output (w)
	
	for i in final_grades:
		txt_out.write('%(percentage)s%%\n' % {"percentage": format(i*10.,'0.2f')})
		if (i < 6.0):
			fail_list.append(i)
		elif (i > 9.5):
			ap_list.append(i)
	
	txt_out.close()
	
	#create human readable versions of failing and outstanding lists of students for output
	
	fail_list_string = []
	ap_list_string = []
	
	for i in fail_list:
		fail_list_string.append('%(percentage)s%%' % {"percentage": format(i*10.,'0.2f')})
	
	
	for i in ap_list:
		ap_list_string.append('%(percentage)s%%' % {"percentage": format(i*10.,'0.2f')})
	
	#begin print number of failing and outstanding students and their grades
	
	print('%(count)d of %(total)d students (%(fract)s%%) failed with less than a 60%%: %(list)s' %
	      {"count": len(fail_list), "total": len(final_grades),
               "fract": format(100.*len(fail_list)/len(final_grades), '0.2f'),
               "list": fail_list_string})
	
	print('%(count)d of %(total)d students (%(fract)s%%) have grades higher than 95%%: %(list)s' %
	      {"count": len(ap_list), "total": len(final_grades),
               "fract": format(100.*len(ap_list)/len(final_grades), '0.2f'),
               "list": ap_list_string})
	
	
	#begin generation of graphs and output to pdf
	
	plt.close()                                             #closes hanging plotting data
	pdf_out = PdfPages('ex2_plots.pdf')                     #opens and initializes a PDF

	# Code for the first page of the PDF file above
	
	plt.figure(figsize=(8.27, 11.69), dpi = 200)            #initializes a A4 size page
	
	plt.subplot2grid((1,1), (0,0))                          #first of one graphs
	plt.hist(final_grades, bins=(0,1,2,3,4,5,6,7,8,9,10), color='blue', label='Final Grades')
	plt.title('Final Grade Histogram')
	plt.xlabel('Grades')
	plt.ylabel('Frequency')
	plt.legend()
	
	plt.tight_layout()                                      #Fixes ovelapping text on page
	pdf_out.savefig()                                       #Prints to the first page
	
	# Code for the second page of the PDF file above
	
	plt.figure(figsize=(8.27, 11.69), dpi = 200)            #initializes a new A4 size page
	
	plt.subplot2grid((3,1), (0,0))                          #first of three graphs
	plt.hist(homework_grades, bins=(0,1,2,3,4,5,6,7,8,9,10), color='red', label='Homework Grades')
	plt.title('Homework Grade Histogram')
	plt.xlabel('Grades')
	plt.ylabel('Frequency')
	plt.legend()
	
	plt.subplot2grid((3,1), (1,0))                          #second of three graphs
	plt.hist(midterm_grades, bins=(0,1,2,3,4,5,6,7,8,9,10), color='red', label='Midterm Grades')
	plt.title('Midterm Grade Histogram')
	plt.xlabel('Grades')
	plt.ylabel('Frequency')
	plt.legend()
	
	plt.subplot2grid((3,1), (2,0))                          #third of three graphs
	plt.hist(final_project_grades, bins=(0,1,2,3,4,5,6,7,8,9,10), color='red',
                 label='Final Project Grades')
	plt.title('Final Project Grade Histogram')
	plt.xlabel('Grades')
	plt.ylabel('Frequency')
	plt.legend()	
	
	plt.tight_layout()                                      #Fixes ovelapping text on page
	pdf_out.savefig()                                       #Prints to the second page
	
	pdf_out.close()                                         #closes opened pdf file
	
	
main()
