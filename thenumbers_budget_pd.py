# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 08:26:26 2020

@author: infomax
"""

import pandas as pd
import numpy as np
#
from scipy import stats
import math
import datetime


dt = pd.read_csv("C:/Users/infomax/Documents/numbers_budget.csv")


# %%
#dt["year"] = 
a = dt["release_date"].astype(str)
dt["year"] = a.str.slice(stop=4)

# %%
dt["rating"] = np.where(dt['mpaa_rating']=='R', 'R', 'PG')

# %%

import matplotlib 
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
%matplotlib qt5

# %%
#import matplotlib 
#matplotlib.use('Qt4Agg')
#%matplotlib qt4

#plt.plot( dt.groupby("year").sort_values(by="year")["year"], dt.groupby("year")..sort_values(by="year")["budget"] )

#dt.plot(kind="bar")

#plt.hist(dt["year"])

#plt.plot(dt.groupby("year")["budget"])

dt2 = dt.set_index(["year","rating"])

rating_list = ["R", "PG" ]

for rating in rating_list :

    year_lim = []
    
    for i in range(10) :
        year_lim.append( ("200" + str(i), rating)  )
    
    for i in range(10) :
        year_lim.append( ("201" + str(i), rating ) )
    
    plt.plot(dt2.loc[year_lim,"budget"].groupby("year").sum(),label="budget " + rating )
    plt.plot(dt2.loc[year_lim,"world_gross"].groupby("year").sum(),label="world_gross " + rating)
plt.legend(fontsize="large")
plt.show()

#dt2.loc[year_lim,"budget"].groupby("year").count()
#dt2.loc[year_lim,"world_gross"].groupby("year").count()

#plt.plot( dt.groupby("year")["year"], dt.groupby("year")["budget"] )