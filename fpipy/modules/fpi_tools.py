import numpy as np
import math

def interpolate(y, x, time):

	"""
	Function to interpolate values between two points on a line
	
	Parameters
	----------
	
	y: float array
		y values to interpolate (entire velocity array not just two points)
		
	x: int array
		time in seconds from first line of sight doppler measurement
		(entire velocity array not just two points)
		
	time: int
		time to get interpolated velocity at in seconds
	"""	

	#find where time is closest to requested time
	index0 = np.where(abs(x - time) == min(abs(x-time)))[0]
	
	#find if closest point is before or after requested time, then get the second index
	if index0 == 0:
		index1 = 1
	elif index0 == len(x)-1:
		index1 = len(x)-2
	elif x[index0] < time:
		index1 = index0 + 1
	else:
		index1 = index0 - 1

	#get x1, x2, y1 and y2 (where 1 is the 1st point in time)
	x1 = x[index0]
	x2 = x[index1]
	y1 = y[index0]
	y2 = y[index1]
	
	#calculate y=mx+c line
	m = (y2-y1)/(x2-x1)
	c = y1 - (m*x1)
	
	#get velociy from requested time
	vel = (m*time) + c

	return vel
		
def hor_vel_calc(losv, losv_time_indexes, zen_v, zen_time_indexes):
	
	"""
	Calculates the horizontal velocity from the line of sight and vertical
	(zenith) velocities
	
	Parameters
	----------
	
	losv: float array
		raw line of sight doppler measurements
		
	losv_time_indexes: int array
		time in seconds from first line of sight doppler measurement
		
	vy: float array
		raw vertical (zenith) velocity measurement
		
	vy_time_indexes: int array
		time in seconds from first line of sight doppler measurements
	"""
	
	if len(losv)+1 != len(zen_v):
		raise Exception("vertical velocity length must be 1 greater than line of sight velocity")
	
	vx = np.empty(len(losv))
	
	for i in range(len(losv)):
		#get vertical velocity at the same time as line of sight measurement
		vy = interpolate(zen_v, zen_time_indexes, losv_time_indexes[i])
		#calculate horizontal velocity
		vx[i] = (losv[i] - (vy*np.sin(np.deg2rad(45)))) / np.cos(np.deg2rad(45))

	return vx

def times_to_secs(dtimes, dtime_min):
	
	"""
	Converts array of times into an array of seconds from a start time
	
	Parameters
	----------
	
	dtimes: array of dtime objects
		array of times to convert (YYYY/MM/DD hh:mm:ss)
		
	dtime_min: dtime object
		start time to compare time computed from
	"""
	
	time_indexes = np.empty(len(dtimes), dtype="int")
	for i in range(len(time_indexes)):
		time_indexes[i] = (dtimes[i]-dtime_min).total_seconds()
		
	return time_indexes

def merge_vecs(NS, EW):
	
	"""
	Calculates the full 2D vector direction and magnitude from North->South and
	East->West flows
	
	Parameters
	----------
	
	NS: float
		velocity of North->South neutral wind flow
		
	EW: float
		velocity of East->West neutral wind flow
	"""
	
	theta = np.rad2deg(np.arctan(NS/EW)) # 90 = E, -90 = W, 0 = N, 180 = S
	print("theta", theta)
	if EW >= 0:
		kvec = 90-theta
	elif EW < 0:
		kvec = -90-theta
	else:
		print("EW must be a number")
		return
	
	velocity = math.sqrt(pow(EW, 2) + pow(NS, 2))
	
	return velocity, kvec