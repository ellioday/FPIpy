#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 08:38:12 2021

@author: elliott
"""

import numpy as np
import os
import h5py
import pydatadarn
import math
import elliotools
import lunapath
import fpipy
import datetime as dt

import madrigalWeb.madrigalWeb

self_path = "/home/elliott/Documents/madrigalWeb-3.2/madrigalWeb/Data/"
fname = self_path+"minime05_uao_20131002.cedar.008.hdf5"

user_fullname = "Elliott Day"
user_email = "e.day1@lancaster.ac.uk"
user_affiliation = "Lancaster University"

madrigalURL = "http://cedar.openmadrigal.org"

def download_data(FPI, date, path):
	
	"""
	Downloads data from the given FPI and date to path
	
	Parameters
	----------
	
	FPI: str
		3-letter abbreviation for FPI station
		
	date: str
		day to obtain data for (YYYY/MM/DD)
		
	path: str
		path to save data file to
		
	Returns
	-------
	
	True (if data was downloaded) or False (if no data was available to download)
	"""
	
	year = int(date[0:4])
	month = int(date[5:7])
	day = int(date[8:10])
	save_name = "{}{}_{}{}{}.hdf5".format(path, FPI, year, month, day)
	
	#get FPI station id
	FPI = fpipy.FPIStation(FPI)
	
	#constants
	user_fullname = "Elliott Day"
	user_email = "e.day1@lancaster.ac.uk"
	user_affiliation = "Lancaster University"
	madrigalURL = "http://cedar.openmadrigal.org"
	
	Data = madrigalWeb.madrigalWeb.MadrigalData(madrigalURL)
	experiment = Data.getExperiments(FPI.id, year, month, day, 0, 0, 0, 
								  year, month, day+1, 0, 0, 0)[0]
	experiment_file = Data.getExperimentFiles(experiment.id)[0]
	if experiment_file.category == 1:
		Data.downloadFile(experiment_file.name, save_name,  user_fullname, 
					user_email, user_affiliation, "hdf5")
		return True
	else:
		return False

class FPIData():

	def __init__(self, FPI, date):
		
		"""
		Collects data from the given FPI and date
		
		Parameters
		----------
		
		FPI: str
			3-letter abbreviation for FPI
			
		date: str
			date to obtain data for (YYYY/MM/DD)
		"""
		
		self.date = date
		#check if data has already been downloaded
		luna_path = lunapath.base_path
		data_path = luna_path+"users/daye1/Madrigal/Data/"
		year = int(date[0:4])
		month = int(date[5:7])
		day = int(date[8:10])
		fname = "{}{}_{}{}{}.hdf5".format(data_path, FPI, year, month, day)
		file_list = os.listdir(data_path)
		#if data has not been downloaded then do it now
		if fname not in file_list:
			download_data(FPI, date, data_path)
		
		#load the data
		self.Table_Layout, self.Data_Params, self.Experiment_Notes, self.Experiment_Params, self.records = self.load_HDF5(fname)
		
		return

	def load_HDF5(self, fname):
		
		"""
		Loads hdf5 data for fabry-perot interferometers
		
		Parameters
		----------
		
		fname: str
			path to hdf5 file.
		"""
	
		with h5py.File(fname, "r") as hdf:
			
			base_items = list(hdf.items())
			
			Data = hdf.get("Data")
			Data_items = list(Data.items())
			Table_Layout = np.array(Data.get("Table Layout"))
			
			#Get Metadata
			Metadata = hdf.get("Metadata")
			Metadata_items = list(Metadata.items())
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
			dtime = elliotools.time_to_dtime(self.times[i])
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
		E_index = np.where(self.azm == 90)
		S_index = np.where(self.azm == 180)
		W_index = np.where(self.azm == -90)
		
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
				#for calculating horizontal velocites we need an extra zenith
				#measurement before the minimu time
				zen_indexes = np.where(zen_dtimes >= dtime_min)[0]
				zen_indexes = np.insert(zen_indexes, 0, min(zen_indexes)-1)
				zen = zen[zen_indexes]
				
				dN = dN[np.where(N_dtimes >= dtime_min)]
				dE = dE[np.where(E_dtimes >= dtime_min)]
				dS = dS[np.where(S_dtimes >= dtime_min)]
				dW = dW[np.where(W_dtimes >= dtime_min)]
				dzen = dzen[zen_indexes]
				
				N_times = N_times[np.where(N_dtimes >= dtime_min)]
				E_times = E_times[np.where(E_dtimes >= dtime_min)]
				S_times = S_times[np.where(S_dtimes >= dtime_min)]
				W_times = W_times[np.where(W_dtimes >= dtime_min)]
				zen_times = zen_times[zen_indexes]
				
				N_dtimes = N_dtimes[np.where(N_dtimes >= dtime_min)]
				E_dtimes = E_dtimes[np.where(E_dtimes >= dtime_min)]
				S_dtimes = S_dtimes[np.where(S_dtimes >= dtime_min)]
				W_dtimes = W_dtimes[np.where(W_dtimes >= dtime_min)]
				zen_dtimes = zen_dtimes[zen_indexes]
				
			if dtime_max !=0:
				
				N = N[np.where(N_dtimes < dtime_max)]
				E = E[np.where(E_dtimes < dtime_max)]
				S = S[np.where(S_dtimes < dtime_max)]
				W = W[np.where(W_dtimes < dtime_max)]
				zen = zen[np.where(zen_dtimes < dtime_max)]				
				
				dN = dN[np.where(N_dtimes < dtime_max)]
				dE = dE[np.where(E_dtimes < dtime_max)]
				dS = dS[np.where(S_dtimes < dtime_max)]
				dW = dW[np.where(W_dtimes < dtime_max)]
				dzen = dzen[np.where(zen_dtimes < dtime_max)]				
				
				N_times = N_times[np.where(N_dtimes < dtime_max)]
				E_times = E_times[np.where(E_dtimes < dtime_max)]
				S_times = S_times[np.where(S_dtimes < dtime_max)]
				W_times = W_times[np.where(W_dtimes < dtime_max)]
				zen_times = zen_times[np.where(zen_dtimes < dtime_max)]
				
		
			return [N, E, S, W, zen, dN, dE, dS, dW, dzen, N_times, E_times, 
					   S_times, W_times, zen_times]
		
		else:
			return [N, E, S, W, dN, dE, dS, dW, dzen]
		
	def hor_vel_calc(self, los_v, los_dtimes, zen_v, zen_dtimes):
		
		"""
		Calculates and returns the horizontal component of the line of sight
		velocity
		
		Parameters
		----------
		
		los_v: float array
			array of line of sight velocities
			
		los_dtimes: dtime array
			array of dtimes of line of sight measurements
			
		zen_v: float array
			array of zenith velocities
			
		zen_dtimes: dtime array
			array of dtimes of zenith measurements
		"""
		
		#convert dtimes to seconds from start time
		year = int(self.date[0:4])
		month = int(self.date[5:7])
		day = int(self.date[8:10])	
		start_dtime = dt.datetime(year, month, day, 0, 0, 0)
		
		#remove los values that are outside of zenith time range
		ix = np.where((los_dtimes >= min(zen_dtimes)) & (los_dtimes <= max(zen_dtimes)))
		los_v = los_v[ix]
		los_dtimes = los_dtimes[ix]
		
		los_time_indexes = np.empty(len(los_v), dtype="int")
		zen_time_indexes = np.empty(len(zen_v), dtype="int")
		for i in range(len(los_v)):
			los_time_indexes[i] = (los_dtimes[i]-start_dtime).total_seconds()
		for i in range(len(zen_v)):
			zen_time_indexes[i] = (zen_dtimes[i]-start_dtime).total_seconds()
			
		#interpolate zenith at locations where we have los measurements
		zen_v_interped = np.interp(los_time_indexes, zen_time_indexes, zen_v)
		
		#calculate horizontal velocity
		hor_v = (los_v - (zen_v_interped*np.sin(np.deg2rad(45)))) / np.cos(np.deg2rad(45))
		
		return hor_v, los_dtimes