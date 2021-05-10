#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:12:54 2021

@author: elliott
"""

import numpy as np
import elliotools



uao_coords = [40.133, elliotools.lon360_to_180(271.8), 0.2] #[glat, glon, alt(km)]
ann_coords = [42.27, elliotools.lon360_to_180(276.25), 0.3] #[glat, glon, alt(km)]
mh_coords = [42.61, elliotools.lon360_to_180(288.52), 0]
eku_coords = [37.75, elliotools.lon360_to_180(275.71), 0.3]
vti_coords = [37.206, elliotools.lon360_to_180(279.58), 0.3]
par_coords = [35.2, elliotools.lon360_to_180(277.15), 0.9]

class FPIStation():
	
	"""
	A class used to access and store hardware data for FPI stations. 
	"""
	
	def __init__(self, FPI_name):
		
		"""
		Parameters
		----------
		
		rad: string
			3 letter station code for requested radar data (e.g. "ann")
			
		Returns
		----------
		
		geographic latitude, geographic longitude (-180 -> 180) and altitude (km)
		"""
		
		self.name = FPI_name
		
		if (FPI_name == "uao") or (FPI_name == "UAO"):
			self.glat = uao_coords[0]
			self.glon = uao_coords[1]
			self.alt = uao_coords[2]
			
		elif (FPI_name == "ann") or (FPI_name == "ANN"):
			self.glat = ann_coords[0]
			self.glon = ann_coords[1]
			self.alt = ann_coords[2]
			
		elif (FPI_name == "mh") or (FPI_name == "MH"):
			self.glat = mh_coords[0]
			self.glon = mh_coords[1]
			self.alt = mh_coords[2]
			
		elif (FPI_name == "eku") or (FPI_name == "EKU"):
			self.glat = eku_coords[0]
			self.glon = eku_coords[1]
			self.alt = eku_coords[2]
			
		elif (FPI_name == "vti") or (FPI_name == "VTI"):
			self.glat = vti_coords[0]
			self.glon = vti_coords[1]
			self.alt = vti_coords[2]
			
		elif (FPI_name == "par") or (FPI_name == "PAR"):
			self.glat = par_coords[0]
			self.glon = par_coords[1]
			self.alt = par_coords[2]
			
		else:
			
			print("Unkown station, parameters unable to load")
		
		return

		
	def get_coords(self, dtime, alt=0, aacgm=True):			
	
		"""
		Calculates and returns aacmgv2 coordinates (mlat, mlon) for this radar 
		for the specified time
		
		Parameters
		----------
		
		time: datetime object
			datetime object of format datetime.datetime(YYYY, MM, DD, hh, mm, ss)
			
		alt: float
			altitude in km
			
		aacgm (optional): bool
			if true will return coords in aacgm coordinates, if false in geographic
		"""

		if aacgm == True:

			#get mlat and mlon
			mlat, mlon = elliotools.geo_to_aacgm(self.glat, self.glon, dtime, self.alt+alt)
			if isinstance(mlat, np.ndarray):
				mlat = mlat[0]
			if isinstance(mlon, np.ndarray):
				mlon = mlon[0]
		
			return mlat, mlon
		
		elif aacgm == False:
			
			return self.glat, self.glon