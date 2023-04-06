# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:57:36 2020

@author: vdegu
"""


import numpy
import math
import matplotlib # import matplotlib first
import datetime
#matplotlib.use('TkAgg')
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#import tkinter
import matplotlib.dates
import matplotlib.pyplot as plt
import pandas

df = pandas.read_csv('Merged/06-02-TC-Merged.csv')

# Def values

num = df.values[:,0]
TA =  df.values[:,2]
TB =  df.values[:,3]
TC1 =  df.values[:,9]
TC5 =  df.values[:,10]
TC6 =  df.values[:,11]
TC4 =  df.values[:,12]



#PLOT BABY ;\ !

fig= plt.figure(figsize=(20,12))
plt.plot(num, TC1, 'm-', label = "TC 1 ")
plt.plot(num, TC5, 'g-', label = "TC 2 ")
#plt.plot(time2, TA, 'c-', label = "TC A ")
#plt.plot(time2, TB, 'b-', label = "TC B ")
plt.plot(num, TC4, 'r-', label = "TC 3")
plt.plot(num, TC6, 'y-', label = "TC 4")

plt.title('06-02 : Experiment Temperature profile ')
plt.axis([0,11000,90,300])
plt.xlabel('time')
plt.ylabel('Temperature (K)')
ax = fig.gca()
ax.set_xticks(num)
ax.set_yticks(numpy.arange(90, 300, 20))
plt.grid()
plt.legend()
plt.show()


#plt.savefig('Temperature-curve.png')