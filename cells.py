# coding=utf8
'''
Created on 5. mar. 2018

@author: ELP
'''
import pandas as pd 
import numpy as np

file = r'Skinnbrokleia_VT71_CellerL.XLSX'
#file = r'edBastø_VT2.xlsx'
#file = r'Korsen_VR51_CellerL.XLSX'
        
df = pd.read_excel(file)
df = df.transpose()

new_df = {'position' : df['position'].values,
            'time' : df['time'].values,
            'Fureflagellater': df['Sum  - Fureflagellater : '].values ,  ## sep
            'Kiselalger' : df['Sum  - Kiselalger : '].values, ## sep   
            'Svepeflagellater' : df['Sum  - Kalk- og svepeflagellater : '],
            'Kiselflagellater' : df['Sum  - Kiselflagellater & Pedineller : '],
            'bluegreenalgae' : df['Sum  - Blågrønnalger : '].values,
            'Svelgflagellater' : df['Sum  - Svelgflagellater : '].values ,
            'Øyealger' : df['Sum  - Øyealger : '].values,
            'Olivengrønnalger' : df['Sum  - Olivengrønnalger : '].values,
            'Uklassifiserte' : df['Sum  - Uklassifiserte : '].values,
            'Myrionecta_rubra' : df['Myrionecta rubra'].values} 

data_df =  pd.DataFrame(new_df)  
data_df['andre'] = df[['Sum  - Blågrønnalger : ',
                       'Sum  - Svelgflagellater : ',
                       'Sum  - Kalk- og svepeflagellater : ',
                       'Sum  - Kiselflagellater & Pedineller : ',
                       'Sum  - Øyealger : ',
                       'Sum  - Olivengrønnalger : ',
                       'Sum  - Uklassifiserte : ',
                       'Myrionecta rubra',
                       'Paulinella ovalis'
                       ]].sum(axis=1)
 
    

import matplotlib.pyplot as plt
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize = (9,4))
ax.plot(data_df.time,data_df['andre'],'go--',label = 'andre')   
ax.plot(data_df.time,data_df['Fureflagellater'],'ro--',label = 'Fureflagellater')   
ax.plot(data_df.time,data_df['Kiselalger'],'ko--',label = 'Kiselalger')   
plt.title(str(file))

plt.legend()
plt.savefig(str(file)+'.png')
#plt.show()

