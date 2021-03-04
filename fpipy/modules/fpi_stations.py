#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:12:54 2021

@author: elliott
"""

import numpy as np
from pydatadarn.utils import coordinate_transformations as coords
from pydatadarn.utils import tools as tools



uao_coords = [40.133, tools.lon360_to_180(278.1), 0.2] #[glat, glon, alt(km)]
ann_coords = [42.27, tools.lon360_to_180(276.25), 0.3] #[glat, glon, alt(km)]

class FPIStation():
	
	"""
	A class used to access and store hardware data for FPI stations. 
	Data is collected from the superdarn rst (required) hdw tables.
	"""
	
	def __init__(self, FPI_name):
		
		"""
		Parameters
		----------
		
		rad: string
			3 letter station code for requested radar data (e.g. "ann")
		"""
		
		self.name = FPI_name
		
		if FPI_name == "uao":
		
			self.glat = uao_coords[0]
			self.glon = uao_coords[1]
			self.alt = uao_coords[2]
			
		elif FPI_name == "ann":
			
			self.glat = ann_coords[0]
			self.glon = ann_coords[1]
			self.alt = ann_coords[2]
			
		else:
			
			print("Unkown station, parameters cannot be loaded")
		
		return

		
	def get_aacgm(self, dtime):			
	
		"""
		Calculates and returns aacmgv2 coordinates for this radar from the
		specified time
		
		Parameters
		----------
		
		time: datetime object
			datetime object of format datetime.datetime(YYYY, MM, DD, hh, mm, ss)
		"""

		#get mlat and mlon
		mlat, mlon = coords.geo_to_aacgm(self.glat, self.glon, dtime, self.alt)
		if isinstance(mlat, np.ndarray):
			mlat = mlat[0]
		if isinstance(mlon, np.ndarray):
			mlon = mlon[0]
		
		return mlat, mlon