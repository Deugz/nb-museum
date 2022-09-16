import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.colors import *
import datetime as dt
import re 								# for alphanumeric sorting
from scipy import *
from scipy import optimize


# Set tags
analysis		= "sample_1_moving_average"
instrument	= "NIMROD"			# "SANDALS" or "NIMROD"
t0	= dt.datetime.now()

if instrument == "SANDALS":
	instrument_tag	= "SLS"			
	q_plot_range	= [0.07, 50]	# x-range for dcs plots
elif instrument == "NIMROD":
	instrument_tag	= "NIMROD000"	
	q_plot_range	= [0.011, 50]	# x-range for dcs plots
else:
	print("\n\n\n------------------------------\n\n\nWARNING\n\ninvalid intrument specified\n\n\n------------------------------\n\n\n")

plot_title 	= "" 
for a in analysis.split("_"):
	plot_title	= plot_title + a + " "
#~ plot_title	= plot_title + "on "+ instrument
print(plot_title)

exceptions		= []

# Get files and labels:
results_file = np.loadtxt("results_%s.txt" %(analysis), unpack=1, dtype="str") #, skiprows = 1, delimiter=","	
# sort all contents read from file into dictionary:
results			= {}
for column in results_file:
	results[column[0]]	= column[1:]

# alphnumeric sorting
def alphanumeric_sort( list ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert 			= lambda text: int(text) if text.isdigit() else text 
    alphanum_key 	= lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 

    return sorted(list, key = alphanum_key)
    
# group files by various keys
# sample
sample_set	= set(results["sample"])
sample_set	= list(sample_set)
sample_set	= alphanumeric_sort(sample_set)
# cycle
cycle_set	= set(results["cycle"])
cycle_set	= list(cycle_set)
cycle_set	= alphanumeric_sort(cycle_set)
# RB_No
RB_No_set	= set(results["RB_No"])
RB_No_set	= list(RB_No_set)
RB_No_set	= alphanumeric_sort(RB_No_set)

# Convert data types:
results["RB_No"]				= results["RB_No"].astype(np.int)
#~ results["files"]				= results["files"].astype(np.int)
files = []
for file_list in results["files"]:
	files.append(int(file_list.split("_")[1]))
results["total_thickness"]	= results["total_thickness"].astype(np.float)
results["tweak_factor"]		= results["tweak_factor"].astype(np.float)
results["times"]				= results["times"].astype(np.float)
results["time_err_neg"]		= results["time_err_neg"].astype(np.float)
results["time_err_pos"]		= results["time_err_pos"].astype(np.float)
results["temperatures"]		= results["temperatures"].astype(np.float)
results["temp_err_neg"]		= results["temp_err_neg"].astype(np.float)
results["temp_err_pos"]		= results["temp_err_pos"].astype(np.float)
for key in results.keys():
	results[key]			= np.array(results[key])

n							= len(results["files"])

# pick only temperature data above 140 K for fit:
temperatures		= []
temp_err_neg		= []
temp_err_pos		= []
tweak_factor		= []
low_temps			= []
low_temp_err_neg	= []
low_temp_err_pos	= []
low_T_tweaks		= []
for i in range(len(results["temperatures"])):
	if (results["temperatures"][i]-results["temp_err_neg"][i] > 140.):
		temperatures.append(results["temperatures"][i])
		temp_err_neg.append(results["temp_err_neg"][i])
		temp_err_pos.append(results["temp_err_pos"][i])
		tweak_factor.append(results["tweak_factor"][i])
	else:
		low_temps.append(results["temperatures"][i])
		low_temp_err_neg.append(results["temp_err_neg"][i])
		low_temp_err_pos.append(results["temp_err_pos"][i])
		low_T_tweaks.append(results["tweak_factor"][i])
temperatures		= np.array(temperatures)
tweak_factor		= np.array(tweak_factor)
low_temps			= np.array(low_temps)
low_T_tweaks		= np.array(low_T_tweaks)

##########          Fitting          ##########

#######     high T:

func	= lambda p,u: 		p[0] + p[1]*u
errfunc 	= lambda p,u,w:	func(p,u) - w
p0		= [6., 0.1]
error	= []

def fit_func(p, temperatures, tweak_factor):
	if (p[1] > 0):
		return errfunc(p, temperatures, tweak_factor)
	else:
		return errfunc(p, temperatures, tweak_factor)+1e100

p1, covariant, infodict, errmsg, success = optimize.leastsq(fit_func, p0, args=(temperatures, tweak_factor), full_output=1)
if (len(temperatures) > len(p0)) and covariant is not None:
	s_sq	= (errfunc(p1, temperatures, tweak_factor)**2).sum()/(len(temperatures)-len(p0))
	covariant = covariant * s_sq
else:
	covariant = inf
for res in range(len(p1)):
	try:
		error.append(np.absolute(covariant[res][res])**0.5)
	except:
		error.append(1e100)

print("tweak = (%.1f +/- %.1f) + (%.1e +/- %.1e) * temp" %(p1[0], error[0], p1[1], error[1]))
#~ print(p1)
#~ print(error)

#Save fit results:
np.savetxt("tweak_factor_fit_%s.txt" %(analysis), np.transpose([p1, error]), fmt=['%1.4e','%1.4e'], newline=os.linesep, header=" p\terror\t(tweak = p[0] + p[1] * temp)")

#######     low T:

#~ low_T_func		= lambda p,u: 		p[0] + p[1]*u + p[2]*u**2
low_T_func		= lambda p,u: 		p[0]+p[1]*np.exp(p[2]*u)	
low_T_errfunc 	= lambda p,u,w:	low_T_func(p,u) - w
low_T_p0		= [1., 0.5, 0.02]
low_T_error		= []

def low_T_fit_func(p, temperatures, tweak_factor):
	if (p[0] > 0) and (p[2] > 0):
		return low_T_errfunc(p, temperatures, tweak_factor)
	else:
		return low_T_errfunc(p, temperatures, tweak_factor)+1e100

low_T_p1, covariant, infodict, errmsg, success = optimize.leastsq(low_T_fit_func, low_T_p0, args=(low_temps, low_T_tweaks), full_output=1)
#~ low_T_p1, covariant, infodict, errmsg, success = optimize.leastsq(low_T_errfunc, low_T_p0, args=(low_temps, low_T_tweaks), full_output=1)
if (len(low_temps) > len(low_T_p0)) and covariant is not None:
	s_sq	= (low_T_errfunc(low_T_p1, low_temps, low_T_tweaks)**2).sum()/(len(low_temps)-len(low_T_p0))
	covariant = covariant * s_sq
else:
	covariant = inf
for res in range(len(low_T_p1)):
	try:
		low_T_error.append(np.absolute(covariant[res][res])**0.5)
	except:
		low_T_error.append(1e100)

#~ print("tweak = (%.1f +/- %.1f) + (%.1e +/- %.1e) * temp" %(p1[0], error[0], p1[1], error[1]))
print(low_T_p1)
print(low_T_error)

##########          Plotting          ##########

##########          tweak factor against temperatures          ##########

# Initialise Gudrun results plot:
fig 			= plt.figure(figsize=(9,6))
fig.patch.set_facecolor("w")					# colour of outer box
plt.subplots_adjust(left=0.085, right=0.99, top=0.96, bottom=0.1)	# margins
ax1			= plt.subplot(111)
# plot_title
ax1.text(0.5,1.0, plot_title, transform=fig.transFigure, horizontalalignment='center', verticalalignment='top', color="k", fontsize=15)
# ax labels
tickfontsize	= 13
ax1.tick_params(which="major", labelsize=tickfontsize)
ax1.tick_params(which="minor", labelsize=tickfontsize)
# x
x_label		= 'Temperature (K)'
ax1.text(0.5,0, x_label, transform=fig.transFigure, horizontalalignment='center', verticalalignment='bottom', color="k", fontsize=15)
# y
y_label		= "Tweak Factor"
ax1.text(0.001,0.5, y_label, transform=fig.transFigure, rotation=90, horizontalalignment='left', verticalalignment='center', color="k", fontsize=15)
# legend
ax1.text(0.4,0.55, "Tweak Factor Fits:", transform=fig.transFigure, horizontalalignment='left', verticalalignment='center', color="k", alpha=0.5, fontsize=13)
ax1.text(0.4,0.5, "(%.1f +/- %.1f) + (%.1e +/- %.1e) * T/K" %(p1[0], error[0], p1[1], error[1]), transform=fig.transFigure, horizontalalignment='left', verticalalignment='center', color="r", alpha=0.5, fontsize=13)
ax1.text(0.4,0.45, "(%.1f +/- %.1f) + (%.1e +/- %.1e) * e$^{(%.3f +/- %.3f) * T/K}$" %(low_T_p1[0], low_T_error[0], low_T_p1[1], low_T_error[1], low_T_p1[2], low_T_error[2]), transform=fig.transFigure, horizontalalignment='left', verticalalignment='center', color="b", alpha=0.5, fontsize=13)

# Plot results:
#~ ax1.plot(results["temperatures"], results["tweak_factor"].astype(np.float), linestyle="", marker="x", color="k")
ax1.errorbar(temperatures, tweak_factor, xerr=[temp_err_neg, temp_err_pos], linestyle="", marker="x", capsize=4, color="r")
ax1.plot(np.linspace(100, 250, 100),  func(p1, np.linspace(100, 250, 100)), color="r", alpha=0.5)
ax1.errorbar(low_temps, low_T_tweaks, xerr=[low_temp_err_neg, low_temp_err_pos], linestyle="", marker="x", capsize=4, color="b")
ax1.plot(np.linspace(70, 250, 100),  low_T_func(low_T_p1, np.linspace(100, 250, 100)), color="b", alpha=0.5)
#~ ax1.plot(np.linspace(70, 250, 100),  low_T_func(low_T_p0, np.linspace(100, 250, 100)), color="k", alpha=0.5)

ax1.set_ylim([0, 90])

plt.savefig("%s_tweak_factor_fit.pdf" %(analysis))
plt.savefig("%s_tweak_factor_fit.png" %(analysis))

#~ plt.show()
plt.close()

