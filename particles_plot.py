'''
Created on 26. jun. 2017

@author: ELP

Script works both for Python 2.7 and Python 3.6, 
but the styles are tuned for Python 2.7 

'''


import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.dates as mdates
from netCDF4 import Dataset, datetime, date2num,num2date

plt.style.use('ggplot')

# Name of netcdf file 

fname = "Kelp_polygon_1_experiment_1_01052016_to_30062016.nc"

fh =  Dataset(fname)

# Read the vaiables from Netsdf 
#varable = np.array(fh.variables['name of variable in NetCDF file'][:])
# to specify dimensions [start:stop]
# 9.96920997e+36 is a value to mask the wrong values (like NaN, -999, etc) 

depth_unmasked = np.array(fh.variables['sea_floor_depth_below_sea_level'][:])
depth_seafloor =  ma.masked_values(depth_unmasked, 9.96920997e+36 )


density = ma.masked_values((np.array(fh.variables['density'][:])), 9.96920997e+36 )
#depth of the particle
z_unmasked = np.array(fh.variables['z'][:]) 
z =  ma.masked_values (z_unmasked, 9.96920997e+36 )
depth = -z


# read the variable with categories of particles (1,2,3,4) according to
# their densities 
category_unmasked = np.array(fh.variables['plantpart'][:])
category = ma.masked_values (category_unmasked,-9223372036854775806 )
time = np.array(fh.variables['time'][:])

#dates = num2date(time[:],units='seconds since 1970-01-01',calendar="standard")
#time = dates 
# different trajectory - different particle 
trajectory  = np.array(fh.variables['trajectory'][:])

sedimentation_depth = []

dif_depth = 5.
tomask_depthes = depth

# mask particles after sedimentation 
for n in trajectory:         
    c = abs(depth_seafloor[n-1] - depth[n-1])   
    #masked_depth = np.ma.where((depth_seafloor[n-1] - (depth[n-1]) <= 1)
    minc = c.min()    
    for k in range(1,len(depth[n-1])):
        dif = depth[n-1][k-1] - depth[n-1][k]
        if dif > 40:
    #if (depth_0[s+1] - depth_0[s]) > 0:  
            tomask_depthes[n-1,k:] = False
        #to remove the surface values     
        #if depth[n-1,k] <1: 
        #    tomask_depthes[n-1,k:] = False        
    
    if minc <= dif_depth :
        
        # get the index of a sedimentation 
        arg = c.argmin() 
        # mask all the values after the settling to the sediment
        tomask_depthes[n-1,arg:] = False
        sedimentation_depth.append((depth_seafloor[(n-1),arg])) 
                 
#depth = tomask_depthes    
depth = ma.masked_where(tomask_depthes == False, tomask_depthes)

#mask particles after "crushing to a wall" 
def sort_by_category(n_cat):
    depth_array = []
    time_array = []
    density_array = []
    
    for n in trajectory:
        #Check if we have densities with negative values  
        #min_dens = ma.min(density[n-1])
        #if min_dens < 0:
        #    print (n)
        # loop over array of categories
        d = ma.min(category[n-1])
        
        if int(d) == int(n_cat):
            # get the depth array for this category
            depth_array.append(depth[n-1]) 
            density_array.append(density[n-1])           
            to_release_depth = ma.array(depth[n-1])
            to_release_time = ma.array(time[n-1])
            # loop over elements of depth array for this trajectory
            for m in np.arange(0,len(to_release_depth)):
                if (to_release_depth[m] is ma.masked) is False:
                # take the index of the first non-masked element
                    #print ('false')
                    release_index = m
                    release_depth = depth[n-1][m]
                    release_time = time[m] 
                    break

            #subtract the time of release from all the time values 
            time_corrected_sec = time - release_time
            #print (num2date(time_corrected_sec,
            #               units="days since 1970-01-01T00:00:00Z",
            #               calendar="standard")) 
            time_corrected_hours = time_corrected_sec/3600.#print (time_corrected)
            #break
            time_array.append(time_corrected_hours)
            
        else : 
            pass 
              
    return depth_array,time_array,density_array
    
# depths_for each category
depth_0 = ma.array(sort_by_category(0)[0])

            
time_0 = ma.array(sort_by_category(0)[1])
time_0 = ma.masked_where(time_0 < 0, time_0)

density_0 = ma.array(sort_by_category(0)[2])

depth_1 = ma.array(sort_by_category(1)[0])
time_1 = ma.array(sort_by_category(1)[1])
time_1 = ma.masked_where(time_1 < 1, time_1)

density_1 = ma.array(sort_by_category(1)[2])

depth_2 = ma.array(sort_by_category(2)[0])
time_2 = ma.array(sort_by_category(2)[1])
time_2 = ma.masked_where(time_2 < 0, time_2)

density_2 = ma.array(sort_by_category(2)[2])

depth_3 = ma.array(sort_by_category(3)[0])
time_3 = ma.array(sort_by_category(3)[1])
time_3 = ma.masked_where(time_3 < 0, time_3)

density_3 = ma.array(sort_by_category(3)[2])

'''      
# make a colorbar 
color_300 ='#ff5555' 
color_1100 = '#14bfb2'
color_2000 = '#0073dc'
colorsList = [(color_300),(color_1100),(color_2000)]
CustomCmap = matplotlib.colors.ListedColormap(colorsList)
'''

def plot_depth_time():
    
    # make a figure
    fig = plt.figure(figsize=(11.69 , 8.27), dpi=100,
                                      facecolor='white')
    
    gs1 = gridspec.GridSpec(2, 2,width_ratios=[10, 1])
    gs1.update(left=0.05, right=0.46, hspace=0.2,wspace=0.05,bottom = 0.1 )
    
    ax0 = fig.add_subplot(gs1[0,0])
    ax0_cb = fig.add_subplot(gs1[0,1])
    ax1 = fig.add_subplot(gs1[1,0])
    ax1_cb = fig.add_subplot(gs1[1,1])    
    

     
    gs2 = gridspec.GridSpec(2, 2,width_ratios=[10, 1])
    gs2.update(left=0.55, right=0.94, hspace=0.2,wspace=0.05,bottom = 0.1 )
   
    ax2 = fig.add_subplot(gs2[0,0])
    ax2_cb = fig.add_subplot(gs2[0,1])    
    
    ax3 = fig.add_subplot(gs2[1,0])
    ax3_cb = fig.add_subplot(gs2[1,1])   

    cmap = plt.get_cmap('OrRd')

    ##Scatter plot 
    
    cs = ax0.scatter(time_0,depth_0, s = density_0/10-100,
                    c = density_0, cmap = cmap,
                    vmin = ma.min(density_0), vmax = ma.max(density_0),
                    alpha = 0.8, )
    ax0.set_title(str(ma.min(density_0)))
    # densities vmin = 1246.6, vmax = 1882.    

    # = plt.colorbar(cs)
    plt.colorbar(cs, cax = ax0_cb)         
           
    cs1 = ax1.scatter(time_1[1:],depth_1[1:],# s = density_1/10-100,
                      c = density_1[1:], cmap = cmap,
                      vmin = ma.min(density_1), vmax = ma.max(density_1))
    ax1.set_title(str(ma.min(density_1)))
    plt.colorbar(cs1, cax = ax1_cb)
    
    cs2 = ax2.scatter(time_2[1:],depth_2[1:], #s = density_2/10-100,
                      c = density_2[1:], cmap = cmap,
                      vmin = ma.min(density_2), vmax = ma.max(density_2))
    ax2.set_title(str(ma.min(density_2)))
    plt.colorbar(cs2, cax = ax2_cb)
    
    cs3 = ax3.scatter(time_3[1:],depth_3[1:], #s = density_3/10-100,
                      c = density_3[1:], cmap = cmap,
                      vmin = ma.min(density_3), vmax = ma.max(density_3))  
    ax3.set_title(str(ma.min(density_3)))  
    plt.colorbar(cs3, cax = ax3_cb)
   
         
    depth_max_0 = depth_0.max()
    depth_max_1 = depth_1.max()
    depth_max_2 = depth_2.max()
    depth_max_3 = depth_3.max()
    
    ax0.set_ylim (depth_max_0,0)
    ax1.set_ylim (depth_max_1,0)
    ax2.set_ylim (depth_max_2,0)
    ax3.set_ylim (depth_max_3,0)     
    

    plt.show()
    #plt.savefig('kelp2_poligon.pdf',format = 'pdf')
    
plot_depth_time()   

import warnings
warnings.simplefilter('error', UserWarning)