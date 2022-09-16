import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.colors import *
import datetime as dt
import re 								# for alphanumeric sorting


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

dcs_plot_range	= [0.25, 400]		# set y-range for dcs plots
#~ dcs_plot_range	= "auto"			# use automatic y-range for dcs plots
dcs_log_scale	= 1					# set to 1 for log-log plots of dcs


# Set directories
Gudrun_directory	= "Gudrun_Results" 

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
for key in results.keys():
	results[key]			= np.array(results[key])

n							= len(results["files"])

##########          Averaging & Residuals          ##########

os.chdir(Gudrun_directory)

# initialise lists & dictionaries
mean_q, intensity, yerr	= np.loadtxt("%s%i.mdcs01" %(instrument_tag, files[0]), unpack=True)
count					= {}
mean_dcs				= {}
sample_residuals			= {}
individual_residuals		= {}
residuals				= []
mean_yerr				= np.zeros(len(mean_q))
count_y					= 0.
for  sample in sample_set:
	count[sample]						= 0.
	mean_dcs[sample]					= np.zeros(len(mean_q))
	sample_residuals[sample]				= np.zeros(len(mean_q))
	individual_residuals[sample]			= {}
	for q in mean_q:
		individual_residuals[sample]["%.4f" %(q)]	= []

# sum all data for each sample
for i in range(len(results["files"])):
	if results["files"][i].split("_")[1] not in exceptions:
		q, intensity, yerr				=	np.loadtxt("%s%i.mdcs01" %(instrument_tag, files[i]), unpack=True)
		mean_dcs[results["sample"][i]]	=	mean_dcs[results["sample"][i]] + intensity
		count[results["sample"][i]]		+=	1.
		mean_yerr						=	mean_yerr + yerr
		count_y							+=	1.

# normalise to number of data sets per sample
for  sample in sample_set:
	for i in range(len(mean_dcs[sample])):
		mean_dcs[sample][i]			=	float(mean_dcs[sample][i])/float(count[sample])
mean_yerr								=	mean_yerr / count_y

# calculate residuals for each scan	
for i in range(len(results["files"])):
	if results["files"][i].split("_")[1] not in exceptions:
		q, intensity, yerr				=	np.loadtxt("%s%i.mdcs01" %(instrument_tag, files[i]), unpack=True)
		residuals.append(np.zeros(len(mean_q)))
		for q in range(len(mean_q)):
			residuals[-1][q]			=	intensity[q] - mean_dcs[results["sample"][i]][q]
			if "%.4f" %(q) in individual_residuals[results["sample"][i]].keys():
				individual_residuals[results["sample"][i]]["%.4f" %(q)].append(residuals[-1][q])
			else:
				individual_residuals[results["sample"][i]]["%.4f" %(q)]	=	[residuals[-1][q]]
	else:
		residuals.append(np.zeros(len(mean_q)))

# calculate max residual range for each sample and each q	
for  sample in sample_set:
	sample_residuals[sample]				=	[]
	for q in range(len(mean_q)):
		sample_residuals[sample].append((np.max(np.array(individual_residuals[sample]["%.4f" %(q)])) - np.min(np.array(individual_residuals[sample]["%.4f" %(q)]))) / 2.)

os.chdir("..")

##########          Plotting          ##########

# Set colormap
cdict = {
		'red':  	((0., 0, 0),		(0.35, 0, 0), 		(0.66, 0.7, 0.7), 	(0.89, 0.8, 0.8),	(1, 0.5, 0.5)	),
		'green':	((0., 0, 0),		(0.125, 0, 0), 		(0.375, 0.7, 0.7),	(0.64, 0.8, 0.8),	(1, 0, 0)		),
		'blue': 	((0., 0.5, 0.5),	(0.11, 0.2, 0.2),	(0.34, 0.8, 0.8), 	(0.65, 0, 0),		(1, 0, 0)		)
		}
colormap = LinearSegmentedColormap('mycolors', cdict)

# Set color cycle & color bar
min_temp			= 90.
max_temp			= 250.
temp_ticks_spacing	= 10.			# minimum for spacing between ticks
color_cycle			= {}
for i in range(len(results["temperatures"])):
	for s in range(len(sample_set)):
		if results["sample"][i] == sample_set[s]:
			color_cycle[results["sample"][i]]	= colormap((float(results["temperatures"][i])-min_temp)/(max_temp - min_temp))
norm 		= mpl.colors.Normalize(vmin=min_temp, vmax=max_temp)
bounds 		= np.linspace(min_temp, max_temp, 500)
plot_ticks	= alphanumeric_sort(results["temperatures"])
while float(plot_ticks[0]) < min_temp:
	print("lowest sample temp below plot range")
	del plot_ticks[0]
while float(plot_ticks[-1]) < min_temp:
	print("highest sample temp below plot range")
	del plot_ticks[-1]
plot_ticks	= np.array(plot_ticks).astype(np.float)
if (max_temp not in plot_ticks) and (abs(plot_ticks[-1]-max_temp) > temp_ticks_spacing) :
	print("max temp added to plot ticks")
	plot_ticks	= np.append(plot_ticks, max_temp)
if (min_temp not in plot_ticks) and (abs(plot_ticks[0]-min_temp) > temp_ticks_spacing) :
	print("min temp added to plot ticks")
	plot_ticks	= np.append(min_temp, plot_ticks)
ax2_label	= "Temperature (K)"

# set x-range for sample_thickness plots, ignoring outliers (from exceptions list)
min_time	= np.max(np.array(results["times"]))
max_time	= np.min(np.array(results["times"]))
for i in range(len(results["files"])):
	if results["files"][i].split("_")[1] not in exceptions:
		if results["times"][i] > max_time:
			max_time	= results["times"][i]
		if results["times"][i] < min_time:
			min_time	= results["times"][i]
full_time				= max_time - min_time
t_plot_range			= [min_time - 0.02 * full_time, max_time + 0.02 * full_time]

# set y-range for sample_thickness plots, ignoring outliers (from exceptions list)
min_thick	= np.max(np.array(results["total_thickness"]))
max_thick	= np.min(np.array(results["total_thickness"]))
for i in range(len(results["files"])):
	if results["files"][i].split("_")[1] not in exceptions:
		if results["total_thickness"][i] > max_thick:
			max_thick		= results["total_thickness"][i]
		if results["total_thickness"][i] < min_thick:
			min_thick		= results["total_thickness"][i]
full_thickness_range			= max_thick - min_thick
# factor 10 converts from cm to mm
sample_thickness_plot_range	= [(min_thick + 0.1 * full_thickness_range) * 10., (max_thick - 0.1 * full_thickness_range) * 10.]

# set y-range for residuals plots, ignoring outliers (from exceptions list)
min_res				= np.max(np.array(residuals[0]))
max_res				= np.min(np.array(residuals[0]))
for i in range(len(results["files"])):
	if results["files"][i].split("_")[1] not in exceptions:
		if np.max(np.array(residuals[i])) > max_res:
			max_res	= np.max(np.array(residuals[i]))
		if np.min(np.array(residuals[i])) < min_res:
			min_res	= np.min(np.array(residuals[i]))
full_residuals_range		= max_res - min_res
if max_res > 0:
	residuals_scale		= 10.**int(math.log10(max_res))/10.
else:
	residuals_scale		= 1.
residuals_plot_range	= [(min_res + 0.1 * full_residuals_range) / residuals_scale, (max_res - 0.1 * full_residuals_range) / residuals_scale]

##########          Plot files against time          ##########
fig 							= plt.figure(figsize=(9,6))
fig.patch.set_facecolor("w")					# colour of outer box
plt.subplots_adjust(left=0.12, right=0.9, top=0.95, bottom=0.12)	# margins
gs 			= gridspec.GridSpec(1, 2,width_ratios=[30,1], hspace=0., wspace=0.05)	# define width ratios of subplots
ax1			= plt.subplot(gs[0])

# ax labels
tickfontsize	= 13
ax1.tick_params(which="major", labelsize=tickfontsize)
ax1.tick_params(which="minor", labelsize=tickfontsize)
# x
x_label		= "Time (h)"
ax1.text(0.5,0, x_label, transform=fig.transFigure, horizontalalignment='center', verticalalignment='bottom', color="k", fontsize=15)
# y
y_label		= "Run Number"
ax1.text(0.001,0.5, y_label, transform=fig.transFigure, rotation=90, horizontalalignment='left', verticalalignment='center', color="k", fontsize=15)

# plot results
for i in range (n):
	if results["files"][i].split("_")[1] in exceptions:
		print ("%s%i (RB%i) not plotted" %(instrument_tag, files[i], results["RB_No"][i]))
	else:
		for s in range(len(sample_set)):
			if results["sample"][i] == sample_set[s]:
				firstfile		= np.min(np.array(results["files"][i][1:].split("_")).astype(np.int))
				lastfile		= np.max(np.array(results["files"][i][1:].split("_")).astype(np.int))
				firsttime	= results["times"][i] - results["time_err_neg"][i]
				lasttime		= results["times"][i] + results["time_err_pos"][i]
				box			= plt.Rectangle([firsttime, firstfile], lasttime-firsttime, lastfile-firstfile , edgecolor=color_cycle[results["sample"][i]], facecolor="None", linewidth=1)
				ax1.add_patch(box)

ax1.errorbar(results["times"], files, xerr=[results["time_err_neg"], results["time_err_pos"]], color="k", linestyle="", marker="", alpha=0)

# Plot color bar
ax2 = plt.subplot(gs[:, -1])
cb = mpl.colorbar.ColorbarBase(ax2, 
						cmap		= colormap,
						norm		= norm,
						boundaries	= bounds,
						ticks		= plot_ticks, # optional
						spacing		= 'proportional',
						orientation	= "vertical")
if temp_ticks_spacing>1:
	ax2.set_yticklabels(["%.0f" %(tick) for tick in plot_ticks], rotation=0, verticalalignment="center", fontsize=tickfontsize)
elif temp_ticks_spacing>0.1:
	ax2.set_yticklabels(["%.1f" %(tick) for tick in plot_ticks], rotation=0, verticalalignment="center", fontsize=tickfontsize)
else:
	ax2.set_yticklabels(["%.2f" %(tick) for tick in plot_ticks], rotation=0, verticalalignment="center", fontsize=tickfontsize)
ax1.text(1.001,0.5, ax2_label, transform=fig.transFigure, rotation=90, horizontalalignment='right', verticalalignment='center', color="k", fontsize=15)

plt.savefig("%s_files_vs_time.pdf" %(analysis))
plt.savefig("%s_files_vs_time.png" %(analysis))
#~ plt.show()
plt.close()

##########          Plot dcs colour coded by temperatures          ##########

# Initialise Gudrun results plot:
fig 			= plt.figure(figsize=(9,6))
fig.patch.set_facecolor("w")					# colour of outer box
plt.subplots_adjust(left=0.085, right=0.92, top=0.96, bottom=0.1)	# margins
gs 			= gridspec.GridSpec(1, 2,width_ratios=[30,1], hspace=0., wspace=0.05)	# define width ratios of subplots
ax1			= plt.subplot(gs[0])
for s in range(len(sample_set)):
	ax1.text(0.87,0.95-(len(sample_set)-s-1.)*0.05, sample_set[s], transform=fig.transFigure, horizontalalignment='right', verticalalignment='top', color=color_cycle[sample_set[s]], fontsize=12)
# plot_title
ax1.text(0.5,1.0, plot_title, transform=fig.transFigure, horizontalalignment='center', verticalalignment='top', color="k", fontsize=15)
# ax labels
tickfontsize	= 13
ax1.tick_params(which="major", labelsize=tickfontsize)
ax1.tick_params(which="minor", labelsize=tickfontsize)
# x
x_label		= 'Q ($\AA^{-1}$)'
ax1.text(0.5,0, x_label, transform=fig.transFigure, horizontalalignment='center', verticalalignment='bottom', color="k", fontsize=15)
# y
y_label		= "Differential Cross Section (barns/sr/atom)"
ax1.text(0.001,0.5, y_label, transform=fig.transFigure, rotation=90, horizontalalignment='left', verticalalignment='center', color="k", fontsize=15)



# Plot Gudrun results:
os.chdir(Gudrun_directory)
for i in range (n):
	if results["files"][i].split("_")[1] in exceptions:
		print ("%s%i (RB%i) not plotted" %(instrument_tag, files[i], results["RB_No"][i]))
	else:
		#Get values and select part.
		q, intensity, yerr	= np.loadtxt("%s%i.mdcs01" %(instrument_tag, files[i]), unpack=True)
		intensity			= intensity
		
		for s in range(len(sample_set)):
			if results["sample"][i] == sample_set[s]:
				ax1.plot(q, intensity, color=color_cycle[results["sample"][i]])
os.chdir("..")

# Plot color bar
ax2 = plt.subplot(gs[:, -1])
cb = mpl.colorbar.ColorbarBase(ax2, 
						cmap		= colormap,
						norm		= norm,
						boundaries	= bounds,
						ticks		= plot_ticks, # optional
						spacing		= 'proportional',
						orientation	= "vertical")
if temp_ticks_spacing>1:
	ax2.set_yticklabels(["%.0f" %(tick) for tick in plot_ticks], rotation=0, verticalalignment="center", fontsize=tickfontsize)
elif temp_ticks_spacing>0.1:
	ax2.set_yticklabels(["%.1f" %(tick) for tick in plot_ticks], rotation=0, verticalalignment="center", fontsize=tickfontsize)
else:
	ax2.set_yticklabels(["%.2f" %(tick) for tick in plot_ticks], rotation=0, verticalalignment="center", fontsize=tickfontsize)
ax1.text(1.001,0.5, ax2_label, transform=fig.transFigure, rotation=90, horizontalalignment='right', verticalalignment='center', color="k", fontsize=15)

# plot range
ax1.set_xlim(q_plot_range)
if dcs_plot_range != "auto":
	ax1.set_ylim(dcs_plot_range)
if dcs_log_scale == 1:
	ax1.set_xscale("log")
	ax1.set_yscale("log")

plt.savefig("%s_mdcs_results.pdf" %(analysis))
plt.savefig("%s_mdcs_results.png" %(analysis))

#~ plt.show()
plt.close()

##########          tweak factor against temperatures          ##########

# Initialise Gudrun results plot:
fig 			= plt.figure(figsize=(9,6))
fig.patch.set_facecolor("w")					# colour of outer box
plt.subplots_adjust(left=0.085, right=0.94, top=0.96, bottom=0.1)	# margins
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

# Plot results:
#~ ax1.plot(results["temperatures"], results["tweak_factor"].astype(np.float), linestyle="", marker="x", color="k")
ax1.errorbar(results["temperatures"].astype(np.float), results["tweak_factor"].astype(np.float), xerr=[results["temp_err_neg"].astype(np.float), results["temp_err_pos"].astype(np.float)], linestyle="", marker="x", capsize=4, color="k")

plt.savefig("%s_tweak_factors.pdf" %(analysis))
plt.savefig("%s_tweak_factors.png" %(analysis))

#~ plt.show()
plt.close()

##########          mean DCS & residuals against q          ##########

# Initialise Gudrun results plot:
fig 			= plt.figure(figsize=(5,12))
fig.patch.set_facecolor("w")					# colour of outer box
plt.subplots_adjust(left=0.19, right=0.91, top=0.97, bottom=0.055)	# margins
gs 			= gridspec.GridSpec(len(sample_set)+2, 1, hspace=0.)	# define width ratios of subplots
axes		= []
for s in range(len(sample_set)):
	axes.append(plt.subplot(gs[len(sample_set)-s-1]))
axes.append(plt.subplot(gs[-2]))
axes.append(plt.subplot(gs[-1]))
# plot_title
axes[0].text(0.5,1., plot_title, transform=fig.transFigure, horizontalalignment='center', verticalalignment='top', color="k", fontsize=15)
# ax labels
tickfontsize	= 11
for ax in axes[:-1]:
	ax.tick_params(which="major", labelsize=tickfontsize, labelbottom="off")
	ax.tick_params(which="minor", labelsize=tickfontsize)
axes[-1].tick_params(which="major", labelsize=tickfontsize)
axes[-1].tick_params(which="minor", labelsize=tickfontsize)
# x
x_label		= 'Q ($\AA^{-1}$)'
axes[0].text(0.5,0, x_label, transform=fig.transFigure, horizontalalignment='center', verticalalignment='bottom', color="k", fontsize=15)
# y
y_label		= "Mean DCS (barns/sr/atom)"
axes[0].text(0.001,0.5, y_label, transform=fig.transFigure, rotation=90, horizontalalignment='left', verticalalignment='center', color="k", fontsize=15)

# more ax labels
for s in range(len(sample_set)):
	axes[s].text(1.03,0.5, sample_set[s], transform=axes[s].transAxes, horizontalalignment='left', verticalalignment='center', rotation=90, color=color_cycle[sample_set[s]], fontsize=12)
axes[-2].text(1.03,0.5, "$\Delta$ y", transform=axes[-2].transAxes, horizontalalignment='left', verticalalignment='center', rotation=90, color="k", fontsize=12)
axes[-1].text(1.03,0.5, "all", transform=axes[-1].transAxes, horizontalalignment='left', verticalalignment='center', rotation=90, color="k", fontsize=12)

# Plot Gudrun results:
os.chdir(Gudrun_directory)
axes[-2].fill_between(mean_q, mean_dcs[sample_set[0]] - mean_yerr, mean_dcs[sample_set[0]] + mean_yerr, color="k", alpha=0.3)
for s in range(len(sample_set)):
	axes[-1].plot(mean_q, mean_dcs[sample_set[s]], color=color_cycle[sample_set[s]])
	axes[s].plot(mean_q, mean_dcs[sample_set[s]], color=color_cycle[sample_set[s]])
	axes[s].fill_between(mean_q, mean_dcs[sample_set[s]] - sample_residuals[sample_set[s]], mean_dcs[sample_set[s]] + sample_residuals[sample_set[s]], color=color_cycle[sample_set[s]], alpha=0.3)

os.chdir("..")

# plot range
for ax in axes:
	ax.set_xlim(q_plot_range)
	twinax	= ax.twinx()
	twinax.tick_params(which="major", labelsize=tickfontsize, labelright="off")
	if dcs_plot_range != "auto":
		ax.set_ylim(dcs_plot_range)
		twinax.set_ylim(dcs_plot_range)
	if dcs_log_scale == 1:
		ax.set_xscale("log")
		ax.set_yscale("log")

plt.savefig("%s_mean_dcs.pdf" %(analysis))
plt.savefig("%s_mean_dcs.png" %(analysis))

#~ plt.show()
plt.close()

##########          DCS & yerr against q          ##########

# Initialise Gudrun results plot:
fig 			= plt.figure(figsize=(5,12))
fig.patch.set_facecolor("w")					# colour of outer box
plt.subplots_adjust(left=0.19, right=0.91, top=0.97, bottom=0.055)	# margins
gs 			= gridspec.GridSpec(len(sample_set), 1, hspace=0.)	# define width ratios of subplots
axes		= []
for s in range(len(sample_set)):
	axes.append(plt.subplot(gs[len(sample_set)-s-1]))
# plot_title
axes[0].text(0.5,1., plot_title, transform=fig.transFigure, horizontalalignment='center', verticalalignment='top', color="k", fontsize=15)
# ax labels
tickfontsize	= 11
for ax in axes[1:]:
	ax.tick_params(which="major", labelsize=tickfontsize, labelbottom="off")
	ax.tick_params(which="minor", labelsize=tickfontsize)
axes[0].tick_params(which="major", labelsize=tickfontsize)
axes[0].tick_params(which="minor", labelsize=tickfontsize)
# x
x_label		= 'Q ($\AA^{-1}$)'
axes[0].text(0.5,0, x_label, transform=fig.transFigure, horizontalalignment='center', verticalalignment='bottom', color="k", fontsize=15)
# y
y_label		= "Mean DCS (barns/sr/atom)"
axes[0].text(0.001,0.5, y_label, transform=fig.transFigure, rotation=90, horizontalalignment='left', verticalalignment='center', color="k", fontsize=15)

# more ax labels
for s in range(len(sample_set)):
	axes[s].text(1.03,0.5, sample_set[s], transform=axes[s].transAxes, horizontalalignment='left', verticalalignment='center', rotation=90, color=color_cycle[sample_set[s]], fontsize=12)

# Plot Gudrun results:
#~ axes[-2].fill_between(mean_q, mean_dcs[sample_set[0]] - mean_yerr, mean_dcs[sample_set[0]] + mean_yerr, color="k", alpha=0.3)
os.chdir(Gudrun_directory)
for i in range (n):
	if results["files"][i].split("_")[1] in exceptions:
		print ("%s%i (RB%i) not plotted" %(instrument_tag, files[i], results["RB_No"][i]))
	else:
		#Get values and select part.
		q, intensity, yerr	= np.loadtxt("%s%i.mdcs01" %(instrument_tag, files[i]), unpack=True)
		intensity			= intensity
		
		for s in range(len(sample_set)):
			if results["sample"][i] == sample_set[s]:
				axes[s].fill_between(q, intensity-yerr, intensity+yerr, color=color_cycle[results["sample"][i]], alpha=0.3)
				axes[s].plot(q, intensity, color=color_cycle[results["sample"][i]])
os.chdir("..")

# plot range
for ax in axes:
	ax.set_xlim(q_plot_range)
	twinax	= ax.twinx()
	twinax.tick_params(which="major", labelsize=tickfontsize, labelright="off")
	if dcs_plot_range != "auto":
		ax.set_ylim(dcs_plot_range)
		twinax.set_ylim(dcs_plot_range)
	if dcs_log_scale == 1:
		ax.set_xscale("log")
		ax.set_yscale("log")

plt.savefig("%s_dcs_uncertainties.pdf" %(analysis))
plt.savefig("%s_dcs_uncertainties.png" %(analysis))

#~ plt.show()
plt.close()
