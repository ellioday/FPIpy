#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 08:38:12 2021

@author: elliott
"""

import numpy as np
import h5py

fpi_path = "/home/elliott/Documents/madrigalWeb-3.2/madrigalWeb/Data/"
fname = fpi_path+"minime05_uao_20131002.cedar.008.hdf5"

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
			print("Items in the base directory:", base_items)
			
			Data = hdf.get("Data")
			Data_items = list(Data.items())
			print("\nItems in Data:", Data_items)
			Table_Layout = np.array(Data.get("Table Layout"))
			
			#Get Metadata
			Metadata = hdf.get("Metadata")
			Metadata_items = list(Metadata.items())
			print("\nItems in Metadata:", Metadata_items)
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
		
		self.Table_layout = np.append(self.Table_Layout, Table)
		self.Data_Params = np.append(self.Data_Params, Data_Params)
		self.Experiment_Notes = np.append(self.Experiment_Notes, Experiment_Notes)
		self.Experiment_Params = np.append(self.Experiment_Params, Experiment_Params)
		self.records = np.append(self.records, records)
		
		return 