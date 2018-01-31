'''
Created on 14. feb. 2017

@author: ELP

Only python 2.7
'''
# TS diagram



import numpy as np
import gsw ### Latest gsw does not support Python < 3.5. 
import matplotlib.pyplot as plt
import csv
import matplotlib.gridspec as gridspec
#from matplotlib import style
plt.style.use('ggplot')
with open('glom171216.txt', 'r') as f:
    reader = csv.reader(f)
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[8:]) )
    sal_temp = r1[2]
    temp_temp = r1[3]
    dens_temp = r1[4]
    press_temp = r1[5] 
    
    salt = []       
    temp = []
    dens = []
    press = []
    
    for n in range(0,len(sal_temp)):
        #Take only samples with salt water
        if np.float(sal_temp[n])> 25.:
            salt.append(np.float(sal_temp[n]))
            temp.append(np.float(temp_temp[n]))
            dens.append(np.float(dens_temp[n]))
            press.append(np.float(press_temp[n]))            
        else:
            pass
 
# Figure out boudaries (mins and maxs)
smin = min(salt) - (0.01 * min(salt))
smax = max(salt) + (0.01 * max(salt))
tmin = min(temp) - (0.1 * max(temp))
tmax = max(temp) + (0.1 * max(temp))
 
# Calculate how many gridcells we need in the x and y dimensions
xdim = int(round((smax-smin)/0.1+1,0))
ydim = int(round((tmax-tmin)+1,0))
 
# Create empty grid of zeros
dens = np.zeros((ydim,xdim))
 
# Create temp and salt vectors of appropiate dimensions
ti = np.linspace(1,ydim-1,ydim)+tmin
si = np.linspace(1,xdim-1,xdim)*0.1+smin
 
# Loop to fill in grid with densities
for j in range(0,int(ydim)):
    for i in range(0, int(xdim)):
        dens[j,i]=gsw.rho(si[i],ti[j],0)
 
# Substract 1000 to convert to sigma-t
dens = dens - 1000
 
# Plot data ***********************************************
#fig1 = plt.figure()
#ax1 = fig1.add_subplot(111)


figure = plt.figure(figsize=(8.69, 8.27), dpi=100)                
gs = gridspec.GridSpec(1,1)
gs.update(wspace=0.1,hspace = 0.2,left=0.1,
       right=0.99,bottom = 0.2, top = 0.9) 

ax00 = figure.add_subplot(gs[0])     
ax00.grid(b=False)
ax00.set_facecolor('#f8f6f1') 


CS = ax00.contour(si,ti,dens, linestyles='dashed',
                   colors='#433f37',linewidth = 1)
plt.clabel(CS, fontsize=12, inline= True , fmt='%1.0f'
           ) # Label every second level
# inline= True breaks the line in a label position.

#ax1.plot(salt,temp,'or', markersize=2,c = press, cmap='bwr')
#ax1.scatter(salt,temp,'or', markersize=2,c = press, cmap='bwr') 

m = ax00.scatter(salt,temp,s = 9, c = press, edgecolor='#59544a', linewidth= 0.2, 
                  cmap='bwr',zorder = 10 )
cbar = plt.colorbar(m, orientation='horizontal')
#cbar = ax00.colorbar(CS)
ax00.set_xlabel('Salinity')
ax00.set_ylabel('Temperature (C)')


#ax01 = figure.add_subplot(gs[1]) 
plt.show()
