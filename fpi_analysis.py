#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:42:24 2021

@author: elliott
"""

import fpi_data
import pydatadarn
import math
import datetime

import numpy as np
import matplotlib.pyplot as plt
import fpi_data as fpd

fpi_path = "/home/elliott/Documents/madrigalWeb-3.2/madrigalWeb/Data/"
fname1 = fpi_path+"minime05_uao_20131001.cedar.010.hdf5"
fname2 = fpi_path+"minime05_uao_20131002.cedar.008.hdf5"

FPI = fpd.FPIData(fname1)

FPI.add_HDF5(fname2)
FPI.get_table()

time_min = "2013/10/02 00:30:00"
time_max = "2013/10/02 08:30:00"
dtime_min = pydatadarn.tools.time_to_dtime(time_min)
dtime_max = pydatadarn.tools.time_to_dtime(time_max)

N, E, S, W, zen, dN, dE, dS, dW, dzen, N_times, E_times, S_times, W_times, zen_times = FPI.get_azm_vels(
	dtime_min = dtime_min, dtime_max = dtime_max)

oN = N
oE = E
oS = S
oW = W

#get dtimes
N_dtimes = pydatadarn.tools.time_to_dtime(N_times)
E_dtimes = pydatadarn.tools.time_to_dtime(E_times)
S_dtimes = pydatadarn.tools.time_to_dtime(S_times)
W_dtimes = pydatadarn.tools.time_to_dtime(W_times)
zen_dtimes = pydatadarn.tools.time_to_dtime(zen_times)

#calculate number of seconds between start and end time
dtime_min = pydatadarn.tools.time_to_dtime(time_min)
dtime_max = pydatadarn.tools.time_to_dtime(time_max)
num_seconds = (dtime_max - dtime_min).seconds

#if we have an array of all seconds between the start and end time
#get the indexes where measurement times match seconds
N_time_indexes = np.empty(len(N), dtype="int")
E_time_indexes = np.empty(len(E), dtype="int")
S_time_indexes = np.empty(len(S), dtype="int")
W_time_indexes = np.empty(len(W), dtype="int")
zen_time_indexes = np.empty(len(zen), dtype="int")

for i in range(len(N)):
	N_time_indexes[i] = (N_dtimes[i]-dtime_min).total_seconds()
for i in range(len(E)):
	E_time_indexes[i] = (E_dtimes[i]-dtime_min).total_seconds()
for i in range(len(S)):
	S_time_indexes[i] = (S_dtimes[i]-dtime_min).total_seconds()
for i in range(len(W)):
	W_time_indexes[i] = (W_dtimes[i]-dtime_min).total_seconds()
for i in range(len(zen)):
	zen_time_indexes[i] = (zen_dtimes[i]-dtime_min).total_seconds()

N, dN = fpd.hor_vel_calc(N, N_time_indexes, zen, zen_time_indexes, dN)
E, dE = fpd.hor_vel_calc(E, E_time_indexes, zen, zen_time_indexes, dE)
S, dS = fpd.hor_vel_calc(S, S_time_indexes, zen, zen_time_indexes, dS)
W, dW = fpd.hor_vel_calc(W, W_time_indexes, zen, zen_time_indexes, dW)

tick_labels = np.array([])

time_tick = dtime_min
minute_interval = 60
while time_tick <= dtime_max:
	hour = time_tick.hour
	minute = time_tick.minute
	tick_labels = np.append(tick_labels, "{:02d}:{:02d}".format(hour, minute))
	time_tick = time_tick + datetime.timedelta(minutes=60)

xlabels = np.array([])
for i in range(0, 11):
	xlables = np.append(xlabels, "00:{:02d}".format(i))

fig, ax = plt.subplots(3, 1, sharex=True)
ax0 = ax[0]
ax1 = ax[1]
ax2 = ax[2]

ax0.errorbar(W_time_indexes, -W, yerr = dW, marker="o", markersize=2.5, label = "West Look")
ax0.errorbar(E_time_indexes, E, yerr = dE, marker="o", markersize=2.5, label = "East Look")
ax0.set_xticks(np.arange(0, num_seconds+minute_interval*60, minute_interval*60))
ax0.set_xticklabels(tick_labels)
#ax0.set_ylim([-150, 100])
ax0.axhline(y=0, color = "k", linestyle = "-.")
ax0.grid(linestyle = "--")
ax0.legend()

ax1.errorbar(S_time_indexes, -S, yerr = dS, marker="o", markersize=2.5, label = "South Look")
ax1.errorbar(N_time_indexes, N, yerr = dN, marker="o", markersize=2.5, label = "North Look")
ax1.axhline(y=0, color = "k", linestyle = "-.")
#ax1.set_ylim([-600, 150])
ax1.grid(linestyle = "--")
ax1.legend()

ax2.errorbar(zen_time_indexes, zen, yerr=dzen, marker="o", markersize=2.5, label = "Zenith")
ax2.axhline(y=0, color = "k", linestyle = "-.")
ax2.set_yticklabels([-600, -450, -300, -150, 0, 150])
ax2.grid(linestyle = "--")
ax2.legend()

plt.show()

"""
FPI1 = fpi_data.FPIData()
FPI2 = fpi_data.FPIData()

FPI1.load_HDF5(fname1)
FPI2.load_HDF5(fname2)

tab1 = FPI1.Table_Layout
tab2 = FPI2.Table_Layout

arrays = [tab1, tab2]

dtype = arrays[0].dtype.descr
new_array = np.append(arrays[0], arrays[1])

newdtype = arrays[0].dtype.descr
newrecarray = np.empty(sum(len(array) for array in arrays), dtype = newdtype)
for array in arrays:
	for name in array.dtype.names:
		newrecarray[name] = array[name]
"""