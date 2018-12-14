'''
Created on 15. nov. 2018

@author: ELP
'''
import pandas as pd
from pyniva import Vessel, TimeSeries, token2header
from pyniva import META_HOST, PUB_META, TSB_HOST, PUB_TSB
import matplotlib.dates as mdates
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import datetime
import numpy as np
import matplotlib.gridspec as gridspec
import json    
path = r'niva-service-account.json'
header = token2header(path)
meta_host = PUB_META
tsb_host = PUB_TSB

def query(vess_name,fname):
    # Get and print list of avaliable vessels 
    vessel_list = [v for v in Vessel.list(meta_host, header=header) if hasattr(v, "imo")] #
    v = [v for v in vessel_list if v.name == vess_name][0]  
    signals = v.get_all_tseries(meta_host, header=header)       

    interesting_signals = ['gpstrack','ctd_salinity'] #'ctd_temperature','ctd_salinity',, 'chla_fluorescence'
    i_signals = [ts for sn in interesting_signals for ts in signals if sn in ts.name]    
    df = TimeSeries.get_timeseries_list(PUB_TSB, i_signals, header=header, ts="P9M", 
                                        dt=0, name_headers=True)        
    df.to_csv(fname)
    
def plot():
    file = 'TFtempsalfluo.csv'
    a = 0.1
    df_tf = pd.read_csv(file)
    df_tf_fluo = pd.read_csv('TFfluo_raw.csv')    
    df_tf_temp= pd.read_csv('TFtemp_raw.csv')  
    df_tf_sal= pd.read_csv('TFsal_raw.csv')      
           
    df_tf = df_tf[df_tf.latitude > 67.5]
    df_tf = df_tf[df_tf.latitude < 69.5]

    df_tf_sal = df_tf_sal[df_tf_sal.latitude > 67.5]
    df_tf_sal = df_tf_sal[df_tf_sal.latitude < 69.5] 
    
    df_tf_fluo = df_tf_fluo[df_tf_fluo.latitude > 67.5]
    df_tf_fluo = df_tf_fluo[df_tf_fluo.latitude < 69.5]    
    
    df_tf_temp = df_tf_temp[df_tf_temp.latitude > 67.5]
    df_tf_temp = df_tf_temp[df_tf_temp.latitude < 69.5]     
    
    fig = plt.figure(figsize=(11.27,5.27), dpi=100)

    ax = plt.subplot2grid((3, 2), (0, 0), rowspan  = 3)
    ax1 = plt.subplot2grid((3, 2), (0, 1), rowspan = 1)    
    ax2 = plt.subplot2grid((3, 2), (1, 1), rowspan = 1)        
    ax3 = plt.subplot2grid((3, 2), (2, 1), rowspan = 1) 
       
    Fmt = mdates.DateFormatter('%b')
    
    map = Basemap(
                resolution='i',projection='stere',\
                lat_0=70,lon_0=14,
                llcrnrlon = 12 ,llcrnrlat = 67,
                urcrnrlon = 21 ,urcrnrlat = 70, ax = ax )
   
    map.drawmapboundary(fill_color='#cae2f7')
    map.fillcontinents(color='#bdad95')
    map.drawcoastlines(linewidth=0.5)
    
    parallels = [67,68,69,70]
    meridians = [5,10,15,20]
    
    map.drawparallels(parallels, labels = [1,1,0,0]) # draw parallels
    map.drawmeridians(meridians, labels = [0,0,1,1]) # draw parallels
    map.scatter(df_tf.longitude.values,df_tf.latitude.values,latlon = True,
                s = 15,ax = ax ,zorder = 5,c='#1e5e75', alpha = 0.7,label = 'TrollFjord \nFerry') #) 
    
    df_tf = df_tf.set_index('time')    
    df_tf.index= pd.to_datetime(df_tf.index)    
    
    df_tf_fluo = df_tf_fluo.set_index('time')    
    df_tf_fluo.index= pd.to_datetime(df_tf_fluo.index)    
    
    df_tf_temp = df_tf_temp.set_index('time').sort_index() 
    df_tf_temp.index= pd.to_datetime(df_tf_temp.index) 

    df_tf_sal = df_tf_sal.set_index('time').sort_index() 
    df_tf_sal.index= pd.to_datetime(df_tf_sal.index) 
           
    df_tf_fluo_1 = df_tf_fluo.where(df_tf_fluo['chla_fluorescence'] < 0.94)
    df_tf_fluo_2 = df_tf_fluo.where(df_tf_fluo['chla_fluorescence'] > 0.96)     
             
    ax1.scatter(df_tf_sal.index, df_tf_sal['ctd_salinity'].values,
                label = 'salinity all',c = '#1e5e75',alpha = a)         
     
    ax2.scatter(df_tf_temp.index, df_tf_temp['ctd_temperature'].values,
                label = 'temperature all raw',c = '#1e5e75',alpha = a)      
      
    ax3.scatter(df_tf_fluo_1.index, df_tf_fluo_1['chla_fluorescence'].values,
                label = 'fluorescence all raw',c = '#1e5e75',alpha = 0.2)       
    ax3.scatter(df_tf_fluo_2.index, df_tf_fluo_2['chla_fluorescence'].values,
                c = '#1e5e75',alpha = 0.2)           
    col = '#b21e1e'
    
    df_1 = pd.read_csv(file)    
    df_1 = df_1.set_index('time')
    df_1.index = pd.to_datetime(df_1.index)
    df_1 = df_1[df_1.latitude > 67.6]
    df_1 = df_1[df_1.latitude < 68] 

    df_tf_sal = df_tf_sal[df_tf_sal.latitude > 67.6]
    df_tf_sal = df_tf_sal[df_tf_sal.latitude < 68] 
    group_sal = df_tf_sal.groupby(df_tf_sal.index.dayofyear).median()
    group_sal.index = pd.to_datetime(group_sal.index,unit = 'D',origin = '2018-01-01')   

    ax1.plot(group_sal.index.values,group_sal['ctd_salinity'].values,c = col,linewidth = 3,
             marker='o',label = 'median ctd_salinity', markeredgecolor = 'k')   
   
    df_tf_temp = df_tf_temp[df_tf_temp.latitude > 67.6]
    df_tf_temp = df_tf_temp[df_tf_temp.latitude < 68] 
    
    group = df_tf_temp.groupby(df_tf_temp.index.dayofyear).median()
    group.index = pd.to_datetime(group.index,unit = 'D',origin = '2018-01-01')

    ax2.plot(group.index.values,group['ctd_temperature'].values,c = col,linewidth = 3,
             marker='o',label = 'median ctd_temperature', markeredgecolor = 'k')    
    map.scatter(df_1.longitude.values,df_1.latitude.values,latlon = True,
                s = 35,ax = ax ,c = col, edgecolors = 'k',zorder = 9,alpha = 1) #) 
        
    df_fluo = pd.read_csv('TFfluo_raw.csv')
    
    df_fluo = df_fluo.set_index('time')
    df_fluo.index = pd.to_datetime(df_fluo.index)
    df_fluo = df_fluo[df_fluo.latitude > 67.6]
    df_fluo = df_fluo[df_fluo.latitude < 68] 

    df_fluo_1 = df_fluo.where(df_fluo['chla_fluorescence'] < 0.94)
    df_fluo_2 = df_fluo.where(df_fluo['chla_fluorescence'] > 0.96)
    df_fluo = pd.concat([df_fluo_1,df_fluo_2],join = 'outer')
    
    group_f = df_fluo.groupby(df_fluo.index.dayofyear).median()
    group_f.index = pd.to_datetime(group_f.index,unit = 'D',origin = '2018-01-01')    

    ax3.plot(group_f.index, group_f['chla_fluorescence'].values,
                label = 'median chla_fluorescence',c = col,linewidth = 3,marker='o',markeredgecolor = 'k') 
        

    r'''with open(r"C:\Users\elp\OneDrive\Python_workspace\climatologyjs\climatology.json") as data_file:    
        data = json.load(data_file)    
 
    d = pd.DataFrame(data)   
    #coord = data['properties']['coordinates']    
        
    days = ["2018-W{}".format(w) for w in d['week']]
    d['days']= [datetime.datetime.strptime(n + '-0', "%Y-W%W-%w") for n in days] 
              
    ax1.plot(d['days'], d['ctd_salinity'].values,label = 'salinity')       
    ax2.plot(d['days'], d['ctd_temperature'].values,label = 'temperature')     
    ax3.plot(d['days'], d['chla_fluorescence'].values,label = 'fluorescence') '''    
    
    axes = (ax,ax1,ax2,ax3)
    for a in axes: 
        a.xaxis.set_major_formatter(Fmt)
        a.legend()    
    plt.tight_layout()
    #plt.show()
    plt.savefig('TF_Ferrybox.png')

#query('MS Trollfjord','TFsal_raw.csv')
#df = pd.read_csv('TF.csv')
#query('M/S Norbjoern','NB2.csv')      
plot()


