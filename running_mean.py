#c48c1b#!/usr/bin/python
# -*- coding: utf-8 -*-
# this ↑ comment is important to have 
# at the very first line 
# to define using unicode
'''
Created on 1. nov. 2017

@author: ELP
'''

import csv
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

import numpy as np
import matplotlib.gridspec as gridspec
from netCDF4 import num2date

## Define colors 
above_0 = '#d87f7f'
below_0 = "#8bafca"
above_0_int = '#7c0000'
below_0_int = "#185f95" 

my_file = 'amon.us.long.data1856-2017.cdc'

def readfile(file):
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        r = []
        for row in reader:
            r.append(row)
        r1 = np.transpose((np.array(r[1:])))
    return (r1)

var = np.array(readfile(my_file))[1:]
var = np.transpose(var)
var = var.ravel()
var = var.astype(np.float)

len_time = 12*(2017 - 1856+1)
time = np.arange(0,len_time)

#var = ma.masked_where(var == -99.990, var)
var = var[:1941] # after 194 all values are invalid 
time = time[:1941]

figure = plt.figure()
gs = gridspec.GridSpec(1,1)
ax00 = figure.add_subplot(gs[0])

ax00.set_xlabel('Time')  
ax00.axhline(0, color='black', linestyle = '--') 

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

# Calculate the mean 
mean = movingaverage(var,12*10)
mean_time = movingaverage(time,12*10)

# Smooth the line 
mean = InterpolatedUnivariateSpline(mean_time, mean)
mean.set_smoothing_factor(0.2)
mean = mean(mean_time)

# to convert num2date in days sine .. 
# since it does not have month as a timedelta 
mean_time = mean_time*30

# Format time axis 
mean_time_format = num2date(mean_time[:], units = 'days since 1856-01-01')
time =  num2date(time[:]*30, units = 'days since 1856-01-01')

# plot all data 
ax00.fill_between(time[:],var[:],0, where = var >= 0., color = above_0, label= u"positive AO")     
ax00.fill_between(time[:],var[:],0, where = var <= 0., color = below_0, label= u"negative AO") 

# plot running mean curve 
ax00.plot(mean_time_format,mean,linewidth = 1,c= 'k',label = '10 year average')

# fill it 
ax00.fill_between(mean_time_format, mean,0, where = mean >= 0., color = above_0_int, alpha = 0.5 )     
ax00.fill_between(mean_time_format, mean,0, where = mean <= 0., color = below_0_int, alpha = 0.5 ) 

plt.legend()
plt.savefig('ao.png')
plt.show()