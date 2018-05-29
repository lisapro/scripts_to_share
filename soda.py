'''
Created on 4. sep. 2017

@author: ELP
'''
# Script to read all the nc files in a folder 
# with different time periods from ROMS
# extracts data from one station 
# combines all time steps and writes to new netcdf 


import os, time
from netCDF4 import MFDataset,Dataset #,num2date,date2num
import numpy as np
import matplotlib.pyplot as plt 
import warnings 

# coordinates of needed station 
#73N 17E, 75N 15E ,58N 11E 

path =  ['''add files here ''']

f = MFDataset(path)
latitude = np.array(f.variables['latitude'])
longitude = np.array(f.variables['longitude'])

# function 'def find_xi_eta' is based on 
# Model2roms  Python toolbox     
# https://github.com/trondkr/model2roms 

def find_xi_eta(st_lon,st_lat):
    """ finds indices for the station close to needed one """

    listd=[]
    listxe=[] 

    for eta in range(len(latitude[:])):
        for xi in range(len(longitude[:])):
            d_lat =  (latitude[eta] - st_lat)
            d_lon =  (longitude[xi] - st_lon)
            distance = np.sqrt(d_lat**2.0 + d_lon**2.0)
            #print (distance)
            listd.append(distance) 
            listxe.append(['xi',xi,'eta',eta])  
            
    value = np.amin(np.array(listd))            
    ind = np.argmin(np.array(listd))   
    xi = listxe[ind][1]  
    eta = listxe[ind][3] 
           
    print (' ')  
    print ('index=',ind,'amin(listd)=',value)
    print (listxe[ind])           
    #print ('long,lat calculated=',longitude[xi],latitude[eta]) 
    #print ('long,lat needed=',st_lon,st_lat)
    
    #print ('indexes', indexes)
    # Here at the first matching index
    # in these data therer are 4 stations 
    # with the same distance from the needed coordinates 
  
    return xi,eta 

def extract_and_plot(st_lon,st_lat): 

    itemindex = find_xi_eta(st_lon,st_lat) 

    xi = itemindex[0]
    eta = itemindex[1] 
    import numpy.ma as ma     
    print (' xi eta', xi,eta)
    print ('long,lat needed=',st_lon,st_lat)    
    print ('long,lat calculated=',longitude[xi],latitude[eta])     
    #Read the data from only one station 
    mlp =  ma.masked_invalid(np.array(f.variables['mlp'][:,eta,xi])) # time is 1 dim
    mls = np.array(f.variables['mls'][:,eta,xi])
    mlt = np.array(f.variables['mlt'][:,eta,xi]) 
    ntime = np.array(f.variables['time'][:])
    #f.close()
        
    import matplotlib.pyplot as plt 
    import pandas as pd
    zipped = list(zip(ntime,[ntime,mlp,mls,mlt]))
    data = dict(zipped)
    df = pd.DataFrame(data)
    
    df.columns = ['month','mlp','mls','mlt']
    #print (df.describe())
    # group stations by month and calculate mean values 
    mean = df.groupby('month').mean()
    mean.plot()
    plt.ylabel('depth')
    #plt.ylim(0,150)
    plt.title('{}N {}E 2010-2015'.format(latitude[eta],longitude[xi]))
    plt.savefig('Mean_Mixed_layer_depth_{}_N_{}_E.png'.format(latitude[eta],longitude[xi]))
    #plt.show()
    plt.clf()
    
    median = df.groupby('month').median()       
    median.plot(subplots = False)    
    plt.ylabel('depth')
    #plt.ylim(0,150)
    plt.title('{}N {}E 2010-2015'.format(st_lat,st_lon))
    plt.savefig('Median_Mixed_layer_depth_{}_N_{}_E.png'.format(st_lat,st_lon))
    plt.clf()
    
# Coordinates of needed stations     
st_lons = [17.0,15.0,11.0]
st_lats = [73.0,75.0,58.0]    

for n in range(0,3): 
    extract_and_plot(st_lons[n],st_lats[n])

if __name__ == '__main__':
    pass