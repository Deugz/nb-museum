import numpy
import math
import matplotlib # import matplotlib first
#matplotlib.use('TkAgg')
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#import tkinter
import matplotlib.pyplot as plt
import pandas

df = pandas.read_csv('../../Merged/03-02-TC-Merged.csv')

# Def values

time = df.values[:,0]
TA =  df.values[:,1]
TB =  df.values[:,2]
TC1 =  df.values[:,8]
TC5 =  df.values[:,9]
TC6 =  df.values[:,10]
#Ethane_intro = 1300
#TC1_subm = 1800
#TC2_subm = 4150
#water_intro_start = 4950
#water_intro_stop = 5550
#end_cooling_time = 1400
#overview_data_x = df.values[:,0] 
#overview_data_y =  df.values[:,8]
#n_nonzero = 0

# TCC loop (Otherwise too few value) --> eliminer les cases vides

#print(TCC)
#count=0
#for i in range(len(TCC)):
#    if TCC[i] > 50.0:
#        count = count +1

#ncc = count

#TCC_new = numpy.zeros(ncc)
#time_new = numpy.zeros(ncc)

#count=0
#for i in range(len(TCC)):
#    if TCC[i] > 50.0:
#        TCC_new[count] = TCC[i]
#        time_new[count] = time[i]
#        print(TCC_new[count], time_new[count])
#        count = count +1

# Temperature mean value def

#TCA_mean = numpy.zeros(end_cooling_time - cooling_time)
#TCB_mean = numpy.zeros(end_cooling_time - cooling_time)

#for i in range(end_cooling_time - cooling_time):
    
#    TCA_mean[i] = TCA[i+cooling_time]

#average_TA = numpy.mean(TCA_mean)
#print(average_TA)

#for i in range(end_cooling_time - cooling_time):
    
#    TCB_mean[i] = TCB[i+cooling_time]

#average_TB = numpy.mean(TCB_mean)
#print(average_TB)

#PLOT BABY ;\ !

fig= plt.figure(figsize=(16,12))
plt.plot(time, TA, 'c-', label = "TA OUT top")
plt.plot(time, TB, 'b-', label = "TB OUT bottom")
plt.plot(time, TC5, 'g-', label = "TC 2 IN top")
plt.plot(time, TC1, 'm-', label = "TC 1 IN bottom")
#plt.plot(time, TC6, 'r-', label = "Thermocouple 4")
#plt.scatter(time_new, TCC_new, c='blue', label = "Thermocouple C")
#plt.axvline(x=Ethane_intro, ls = ':' ,label = "Ethane intro = {0} s".format(int(Ethane_intro) ))
#plt.axvline(x=TC1_subm, ls = ':' ,label = "TC1 submerged = {0} s".format(int(TC1_subm) ))
#plt.axvline(x=TC2_subm, ls = ':' ,label = "TC2 submerged = {0} s".format(int(TC2_subm) ))
#plt.axvline(x=water_intro_start, ls = ':' ,label = "water_intro_start = {0} s".format(int(water_intro_start) ))
#plt.axvline(x=water_intro_stop, ls = ':' ,label = "water_intro_stop = {0} s".format(int(water_intro_stop) ))
#plt.axhline(y=average_T1,label = "T1 mean = {0} K".format(int(average_T1) ))
#plt.axhline(y=average_TB,label = "TB mean = {0} K".format(int(average_TB) ))
plt.title('03-02 Cooling ')
plt.axis([420,2040,90,240])
plt.xlabel('time(s)')
plt.ylabel('Temperature (K)')
ax = fig.gca()
ax.set_xticks(numpy.arange(420, 2040,60))
ax.set_yticks(numpy.arange(90, 240, 10))
plt.grid()
plt.legend()
plt.show()


#plt.savefig('Temperature-curve.png')