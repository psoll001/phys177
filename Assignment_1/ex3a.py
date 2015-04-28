import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def dropped_distance_traveled(v,t):
	#values must be in meters and seconds respectively
	return v +(0.5 * 9.81 * t * t)

def time_to_fall(v, x):
	return (np.sqrt(19.62*x+v*v)-v)/9.81

def dropped_velocity(t):
	return (9.81 * t)

def main():
	
	initial_velocity = 0.0
	burj_khalifa_height = 800.0  #height in meters
	
	input_check = False
	while not(input_check):
		try:
		  initial_velocity = float(input('Enter an initial downward velocity to throw '
                                                 'something off of a 800m tower: '))
		  input_check = isinstance(initial_velocity, float)
		except ValueError as err:
		  print('Error: %(val)s\n' % {"val": err})
		
	time_t = time_to_fall(initial_velocity, burj_khalifa_height)
	
	print('Time until the ball reaches the ground: %(val)s seconds' % 
	      {"val": format(time_t, '.03f')})
	
	
main()
