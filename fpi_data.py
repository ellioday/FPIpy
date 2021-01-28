#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 08:38:12 2021

@author: elliott
"""

import numpy as np
import h5py
import pydatadarn

self_path = "/home/elliott/Documents/madrigalWeb-3.2/madrigalWeb/Data/"
fname = self_path+"minime05_uao_20131002.cedar.008.hdf5"

class FPIData():

	def __init__(self, fname):
		
		self.Table_Layout, self.Data_Params, self.Experiment_Notes, self.Experiment_Params, self.records = self.load_HDF5(fname)
		
		return

	def load_HDF5(self, fname):
		
		"""
		Loads and saves hdf5 data for fabry-perot interferometers
		
		Parameters
		----------
		
		fname: str
			path to hdf5 file.
		"""
	
		with h5py.File(fname, "r") as hdf:
			
			base_items = list(hdf.items())
			#print("Items in the base directory:", base_items)
			
			Data = hdf.get("Data")
			Data_items = list(Data.items())
			#print("\nItems in Data:", Data_items)
			Table_Layout = np.array(Data.get("Table Layout"))
			
			#Get Metadata
			Metadata = hdf.get("Metadata")
			Metadata_items = list(Metadata.items())
			#print("\nItems in Metadata:", Metadata_items)
			Data_Params = np.array(Metadata.get("Data Parameters"))
			Experiment_Notes = np.array(Metadata.get("Experiment Notes"))
			Experiment_Params = np.array(Metadata.get("Experiment Parameters"))
			records = np.array(Metadata.get("_record_layout"))
			
			return [Table_Layout, Data_Params, Experiment_Notes,
					   Experiment_Params, records]
	
	def add_HDF5(self, fname):
		
		"""
		Adds new file to currently saved Data
		
		Parameters
		----------
		fname: str
			path to hdf5 file to add.
		"""
		
		[Table, Data_Params, Experiment_Notes, Experiment_Params, records] = self.load_HDF5(fname)
		
		self.Table_Layout = np.append(self.Table_Layout, Table)
		self.Experiment_Notes = np.append(self.Experiment_Notes, Experiment_Notes)
		self.Experiment_Params = np.append(self.Experiment_Params, Experiment_Params)
		self.records = np.append(self.records, records)
		
		return
	
	def get_table(self):
		
		self.year = np.array(self.Table_Layout["year"], dtype = "int")
		self.month = np.array(self.Table_Layout["month"], dtype= "int")
		self.day = np.array(self.Table_Layout["day"], dtype = "int")
		self.hour = np.array(self.Table_Layout["hour"], dtype = "int")
		self.min = np.array(self.Table_Layout["min"], dtype = "int")
		self.sec = np.array(self.Table_Layout["sec"], dtype = "int")
		self.recno = np.array(self.Table_Layout["recno"], dtype = "int")
		self.kindat = np.array(self.Table_Layout["kindat"], dtype = "int")
		self.kinst = np.array(self.Table_Layout["kinst"], dtype = "int")
		self.elm = np.array(self.Table_Layout["elm"], dtype = "int")
		self.azm = np.array(self.Table_Layout["azm"], dtype = "int")
		self.gdalt = np.array(self.Table_Layout["gdalt"], dtype = "int")
		self.temp = np.array(self.Table_Layout["tn"], dtype = "int")
		self.dtemp = np.array(self.Table_Layout["dtn"], dtype = "int")
		self.los_v = np.array(self.Table_Layout["vnu"], dtype = "float")
		self.dlos_v = np.array(self.Table_Layout["dvnu"], dtype = "float")
		self.temp_err = np.array(self.Table_Layout["temp_err"], dtype = "int")
		self.wind_err = np.array(self.Table_Layout["wind_err"], dtype = "int")
		
		self.times = np.array([])
		for i in range(len(self.year)):
			string_time = "{:02d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(self.year[i], self.month[i], self.day[i], self.hour[i], self.min[i], self.sec[i])
			self.times = np.append(self.times, string_time)
		
		self.dtimes = np.array([])
		for i in range(len(self.times)):
			dtime = pydatadarn.utils.tools.time_to_dtime(self.times[i])
			self.dtimes = np.append(self.dtimes, dtime)
		return
	
	def get_azm_vels(self, dtime_min = 0, dtime_max = 0):
		
		"""
		Returns the North, East, South, West and Zenith line of sight velocities
		respectively
		
		Parameters
		----------
		dtime_min (optional): dtime object
			minimum time to get data for
		dtime_max (optional): dtime object
			maximum time to get data for
		"""
		
		#get indexes of east, south and west look
		E_index = np.where(self.azm == -90)
		S_index = np.where(self.azm == 180)
		W_index = np.where(self.azm == 90)
		
		#get indexes of 0 azimuth (could be north or zenith look)
		zero_index = np.where(self.azm == 0)
		#get indexes of north or zenith look
		N_elm_index = np.where(self.elm == 45)
		#zenith indexes are where elevation angles are at 90deg
		zen_index = np.where(self.elm == 90)
		#north indexes are where azm == 0 and elm == 45
		N_index = np.intersect1d(zero_index, N_elm_index)
		
		#get velocity data
		N = self.los_v[N_index]
		E = self.los_v[E_index]
		S = self.los_v[S_index]
		W = self.los_v[W_index]
		zen = self.los_v[zen_index]
		
		#get error in velocity data
		dN = self.dlos_v[N_index]
		dE = self.dlos_v[E_index]
		dS = self.dlos_v[S_index]
		dW = self.dlos_v[W_index]
		dzen = self.dlos_v[zen_index]
		
		if dtime_min !=0 or dtime_max !=0:
		
			N_times = self.times[N_index]
			E_times = self.times[E_index]
			S_times = self.times[S_index]
			W_times = self.times[W_index]
			zen_times = self.times[zen_index]
		
			N_dtimes = self.dtimes[N_index]
			E_dtimes = self.dtimes[E_index]
			S_dtimes = self.dtimes[S_index]
			W_dtimes = self.dtimes[W_index]
			zen_dtimes = self.dtimes[zen_index]
			
			if dtime_min !=0:
				
				N = N[np.where(N_dtimes >= dtime_min)]
				E = E[np.where(E_dtimes >= dtime_min)]
				S = S[np.where(S_dtimes >= dtime_min)]
				W = W[np.where(W_dtimes >= dtime_min)]
				zen = zen[np.where(zen_dtimes >= dtime_min)]
				
				dN = dN[np.where(N_dtimes >= dtime_min)]
				dE = dE[np.where(E_dtimes >= dtime_min)]
				dS = dS[np.where(S_dtimes >= dtime_min)]
				dW = dW[np.where(W_dtimes >= dtime_min)]
				dzen = dzen[np.where(zen_dtimes >= dtime_min)]
				
				N_times = N_times[np.where(N_dtimes >= dtime_min)]
				E_times = E_times[np.where(E_dtimes >= dtime_min)]
				S_times = S_times[np.where(S_dtimes >= dtime_min)]
				W_times = W_times[np.where(W_dtimes >= dtime_min)]
				zen_times = zen_times[np.where(zen_dtimes >= dtime_min)]
				
			if dtime_max !=0:
				
				N = N[np.where(N_dtimes <= dtime_max)]
				E = E[np.where(E_dtimes <= dtime_max)]
				S = S[np.where(S_dtimes <= dtime_max)]
				W = W[np.where(W_dtimes <= dtime_max)]
				zen = zen[np.where(zen_dtimes <= dtime_max)]				
				
				dN = dN[np.where(N_dtimes <= dtime_max)]
				dE = dE[np.where(E_dtimes <= dtime_max)]
				dS = dS[np.where(S_dtimes <= dtime_max)]
				dW = dW[np.where(W_dtimes <= dtime_max)]
				dzen = dzen[np.where(zen_dtimes <= dtime_max)]				
				
				N_times = N_times[np.where(N_dtimes <= dtime_max)]
				E_times = E_times[np.where(E_dtimes <= dtime_max)]
				S_times = S_times[np.where(S_dtimes <= dtime_max)]
				W_times = W_times[np.where(W_dtimes <= dtime_max)]
				zen_times = zen_times[np.where(zen_dtimes <= dtime_max)]
		
			return [N, E, S, W, zen, dN, dE, dS, dW, dzen, N_times, E_times, 
					   S_times, W_times, zen_times]
		
		else:
			return [N, E, S, W, dN, dE, dS, dW, dzen]