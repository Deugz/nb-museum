import subprocess
import os
import time
import datetime as dt
from datetime import timedelta
import numpy as np

''' 
--------------------------------------------------------------------------------------------------------------
	2018: Sabrina Gaertner
--------------------------------------------------------------------------------------------------------------
This script runs Gudrun for a number of specified files in the <analysis>.csv file.
This script is specifically designed for the amorphous icy particles data where a changing camount of ethane contamination occurs.
The script will read from a file the water tweak factor and process data based on that.
For T < 140 K, ethane will be addedd to the analysis.
The script will adjust the ethane amount together with the tweak factors/atomic number density until the DCS level is within specified range of expected level.
The script will change the sample thickness to the one specified below, but not fit it to achieve DCS match.
(Change below settings as required.)

This script processes multiple files to be averaged in Gudrun.

Before starting:
	1) Create the gudrun_dcs.dat file from the Gudrun gui, choosing the right instrument and naming the (one) 
	   SAMPLE tab "Sample" and the CONTAINER tab "Can" 
	   (by setting everything in gudrun ready to run analysis and saving the txt file).
	2) Make sure that gudrun_dcs.dat is in the directory where gudrun results should be written and
	   also copy the gudrun_dcs.exe file from Gudrun's bin directory there.
	3) Set results_directory to the directory where you want Gudrun to write the results.
	4) Create (or update) the excel sheet containing the summary of the data to be analysed:
		a) Copy relevant data across from JournalViewer, keep the column headings from the original Excel sheet for these columns.
		b) Add column headings for each sample you want to analyse.
		c) Assign each row (i.e. each scan) to one of the samples by adding an "X" in the respective column 
		   (can be automated in Excel to some degree).
		d) Add caveats in the final "note" column, where necessary. 
		   These files will be analysed, but the results will be written to a separate file.
		e) Make sure to replace any commas with "/"
		   (otherwise the reading of comma separated values will get confused).
		f) Save the resulting file as BOTH .xls/.xlsx AND .csv
		   (the csv is read by the Python script, but any formatting and automated filling, 
		   which you may need for future reference will only work in .xls/.xlsx format).
	5) Check the entries in <analysis> and <instrument> are up-to-date.
--------------------------------------------------------------------------------------------------------------
'''

# Identification tags for filenames:
analysis					= "sample_1_ethane_amount_moving_average"
instrument				= "NIMROD"			# "SANDALS" or "NIMROD"
water_tweak_analysis	= "sample_1_moving_average"

# maximum number of files to be averaged:
N_average				= 500

# file_tags:
if instrument == "SANDALS":
	instrument_tag		= "SLS"	
	dcs_line_number	= 44
elif instrument == "NIMROD":
	instrument_tag	= "NIMROD000"	
	dcs_line_number	= 51
else:
	print("\n\n\n------------------------------\n\n\nWARNING\n\ninvalid intrument specified\n\n\n------------------------------\n\n\n")

# Directories:
work_directory			= os.getcwd()
results_directory		= os.getcwd() + "/Gudrun_Results"
data_directory			= "//isis/inst$/NDX%s/instrument/data" %(instrument)

water_tweak_directory	= "../" 
for tag in water_tweak_analysis.split("_")[2:-1]:
	water_tweak_directory += tag
	water_tweak_directory += "_"
water_tweak_directory += water_tweak_analysis.split("_")[-1]
print()

#~ # Time (use current time as reference to calculate time in between scans):
#~ t0	= dt.datetime.now()
# Time (use first time stamp on first scan as reference to calculate time in between scans, update manually):
t0	= dt.datetime.strptime("2018-05-04T01:55:15", "%Y-%m-%dT%H:%M:%S")
# data aquisition times
times			= []					# actual times from log files
time_err		= [[], []]				# strongest time deviations during these scans
# temperatures
temperatures	= []					# actual temperatures from log files
temp_err		= [[], []]				# strongest temp deviations during these scans

# Get water_tweak fit:
os.chdir(water_tweak_directory)
tweak_fit_params, tweak_fit_err = np.loadtxt("tweak_factor_fit_%s.txt" %(water_tweak_analysis), unpack=1, dtype="str") #, skiprows = 1, delimiter=","	
os.chdir(work_directory)

# Sample properties:
#~ can_volume					= 3.116						# sample can volume in ml=cm^3
#~ water_tweak				= 60.							# water tweak factor -> eventually look this up from file
water_density				= 0.095						# atomic density of water (atoms/angstrom^3)
D_inc_scatt_len				= 4.04							# incoherrent scattering length D in 10^-15 m from NIST
ethane_density				= 0.112311						# atomic density of ethane (atoms/angstrom^3)
H_inc_scatt_len				= 25.274						# incoherrent scattering length H in 10^-15 m from NIST
# Start values for thickness and tweak_factor:
#~ tweak_factor_save_to_file	= water_tweak
#~ tweak_factor				= tweak_factor_save_to_file		# 1/volume filling
thickness_save_to_file		= 0.2							# sample thickness (cm)
thickness					= thickness_save_to_file/2.		# half of sample thickness (cm), as required by Gudrun
thickness					= str(thickness) + "  " + str(thickness)

# Files to analyse:
excel_contents	= np.loadtxt("%s.csv" %(analysis), unpack=True, dtype="str", delimiter=",", skiprows=1)
# sort all contents read from Excel into dictionary:
input			= {}
for column in excel_contents:
	input[column[0]]	= column[1:]

# readout samples
sample		= []
for i in range(len(input["Run"])):
	for key in list(input.keys()):
		if input[key][i] == "X":
			sample.append(key)
sample_set	= set(sample)

# Assign new RB_No to calibration scans with RB_No "0". Format 1520 for cycle 15_2:
for i in range(len(input["RB_No"])):
	if input["RB_No"][i] == "0":
		input["RB_No"][i] = input["Cycle"][i].split("_")[0] + input["Cycle"][i].split("_")[1] + "0"

# Get normalisation & background data for each RB_No
rb_numbers			= set(input["RB_No"])
print("RB_No:", rb_numbers)
normalisations			= {}
empty_instruments		= {}
sample_environment	= {}
empty_can				= {}
for rb in rb_numbers:
	normalisations[rb]			= []
	empty_instruments[rb]		= []
	sample_environment[rb]	= []
	empty_can[rb]	= []
for i in range(len(input["Run"])):
	if input["VNb"][i]:
		normalisations[input["RB_No"][i]].append(input["Run"][i])
	elif input["Instr"][i]:
		empty_instruments[input["RB_No"][i]].append(input["Run"][i])
	elif input["CCR"][i]:
		sample_environment[input["RB_No"][i]].append(input["Run"][i])
	elif input["empty_can"][i]:
		empty_can[input["RB_No"][i]].append(input["Run"][i])

print("\nnormalisations", normalisations)
print("\nempty_instruments", empty_instruments)
print("\nsample_environment", sample_environment)
print("\nempty_can", empty_can)

# Sort individual scans into sub-sets to be averaged over (separated by RB_No):
# 			note: this will not work for data from the same RB_No taken over different cycles
sample_sub_sets		= {}
sample_sub_set_cycles	= {}

for Sample in sample_set:
	for i in range(len(input["Run"])):
		if (input[Sample][i] == "X"):
			if Sample not in sample_sub_sets.keys():
				sample_sub_sets[Sample]	= {}
				sample_sub_set_cycles[Sample]	= {}
			if input["RB_No"][i] not in sample_sub_sets[Sample].keys():
				sample_sub_sets[Sample][input["RB_No"][i]]	= [[]]
				sample_sub_set_cycles[Sample][input["RB_No"][i]]	= input["Cycle"][i]
			if input["Run"][i] not in sample_sub_sets[Sample][input["RB_No"][i]][-1]:
				if len(sample_sub_sets[Sample][input["RB_No"][i]][-1]) == N_average:
					sample_sub_sets[Sample][input["RB_No"][i]].append([])
				if input["note"][i] == True:
					print("Skipped scan %i, RB%s, Cycle %s" %(input["Run"][i], input["RB_No"][i], input["Cycle"][i]))
					print("Note:\n" + input["note"][i])
				else:
					sample_sub_sets[Sample][input["RB_No"][i]][-1].append(input["Run"][i])

# Initialise Output
output 		= []
output.append("#used DCS level to determine ethane amount, based on a D2O tweak factor fit for pure D2O samples at higher T\n")
output.append("#tweak_factor_fit_%s.txt\t: tweak = (%s +/- %s) + (%s +/- %s) * temp\n" %(water_tweak_analysis, tweak_fit_params[0], tweak_fit_err[0], tweak_fit_params[1], tweak_fit_err[1]))
output.append("#ethane_water_ratio = number of ethane molecules per water molecule\n")
output.append("cycle\tRB_No\tsample\tfiles\ttotal_thickness\ttweak_factor\tatomic_number_density\tethane_water_ratio\twater_tweak\ttimes\ttime_err_neg\ttime_err_pos\ttemperatures\ttemp_err_neg\ttemp_err_pos\n")
output.append("#\t\t(cm)\t\t(atoms/angstrom^3)\t\t\t(h)\t(h)\t(h)\n")

analysis_issues_output	= []
issues					= 0

def change_sample_composition(dcs_content, count, tweak_factor, suggested_tweak):
	# Get entries in dcs file that refer to the right tab:
	tab_start							= "SAMPLE Sample          {\n"
	tab_end							= "\n}"
	dcs_content_sample					= dcs_content.split(tab_start)[-1]
	dcs_content_sample					= dcs_content_sample.split(tab_end)[0]
	dcs_content_sample1				= dcs_content_sample
	#Get sample composition.
	dcs_content_sample_compostion		= dcs_content_sample.split("1          Force calculation of sample corrections?\n")[1]
	dcs_content_sample_compostion		= dcs_content_sample_compostion.split("\n*  0  0          * 0 0 to specify end of composition input")[0]
	dcs_content_sample_compostion1	= dcs_content_sample_compostion
	for composition_line in dcs_content_sample_compostion1.split("\n"):
		if "H  2" in composition_line:
			dcs_content_deuterium1	= composition_line
			deuterium_amount			= dcs_content_deuterium1.split("  ")[2]
		elif "O  0" in composition_line:
			dcs_content_oxygen1		= composition_line
			oxygen_amount				= dcs_content_oxygen1.split("  ")[2]
		elif "C  0" in composition_line:
			dcs_content_carbon1		= composition_line
			carbon_amount				= dcs_content_carbon1.split("  ")[2]
		elif "H  0" in composition_line:
			dcs_content_hydrogen1		= composition_line
			hydrogen_amount			= dcs_content_hydrogen1.split("  ")[2]
		else:
			print("non matching composition line found: check gudrun_dcs.dat")
			print(composition_line)
	if count == 0:
		# Change composition back to pure D2O
		new_hydrogen_amount			= 0.
		new_carbon_amount			= 0.
	elif (count == 1) and (suggested_tweak < tweak_factor):
		# introduce ethane to the composition
		new_hydrogen_amount			= 2.*float(deuterium_amount)*3. * (D_inc_scatt_len/H_inc_scatt_len)**2 * (water_tweak/float(suggested_tweak) - 1)
		new_carbon_amount			= new_hydrogen_amount/3. 
	elif count > 1:
		# adjust ethane amount
		new_hydrogen_amount			= float(hydrogen_amount) * (tweak_factor/float(suggested_tweak))
		new_carbon_amount			= new_hydrogen_amount/3. 
	else:
		# Change composition back to pure D2O
		new_hydrogen_amount			= 0.
		new_carbon_amount			= 0.
		iterate_gudrun					= 0
	dcs_content_carbon					= "C  0  %.5f          Sample atomic composition" %(new_carbon_amount)
	dcs_content_hydrogen				= "H  0  %.5f          Sample atomic composition" %(new_hydrogen_amount)
	print("deuterium_amount\t= %s" %(deuterium_amount))
	print("oxygen_amount\t\t= %s" %(oxygen_amount))
	print("carbon_amount\t\t= %s" %(new_carbon_amount))
	print("hydrogen_amount\t= %s" %(new_hydrogen_amount))
	dcs_content_sample_compostion		= dcs_content_sample_compostion.replace(dcs_content_carbon1, dcs_content_carbon)
	dcs_content_sample_compostion		= dcs_content_sample_compostion.replace(dcs_content_hydrogen1, dcs_content_hydrogen)
	dcs_content_sample					= dcs_content_sample1.replace(dcs_content_sample_compostion1, dcs_content_sample_compostion)
	dcs_content							= dcs_content.replace(dcs_content_sample1, dcs_content_sample)
	
	if count > 0:
		ethane_fraction			= (new_carbon_amount + new_hydrogen_amount)/(float(deuterium_amount) + float(oxygen_amount))
		atomic_number_density	= (water_density * ethane_density * (ethane_fraction + 1))/(water_density * ethane_fraction + ethane_density)
		tweak_factor			= ethane_density * water_tweak / (water_density * ethane_fraction + ethane_density)
		print("\nethane fraction:\t%s" %(ethane_fraction))
		ethane_water_ratio		= new_carbon_amount / float(deuterium_amount)
	else: 
		atomic_number_density	= water_density
		ethane_water_ratio		= 0
		
	return dcs_content, atomic_number_density, tweak_factor, ethane_water_ratio

def change_tweak_and_density(dcs_content, atomic_number_density, tweak_factor):
	# Get entries in dcs file that refer to the right tab:
	tab_start					= "SAMPLE Sample          {\n"
	tab_end					= "\n}"
	dcs_content_sample			= dcs_content.split(tab_start)[-1]
	dcs_content_sample1		= dcs_content_sample.split(tab_end)[0]
	# Get tweak_factor:
	dcs_content_tweak_factor	= dcs_content_sample.split("Total cross section source")[1]
	dcs_content_tweak_factor	= dcs_content_tweak_factor.split("0          Top hat width")[0]
	tweak_factor1				= dcs_content_tweak_factor.split("          ")[0][1:]
	#Change tweak_factor.
	tweak_factor				= str(tweak_factor)
	dcs_content_tweak_factor1	= dcs_content_tweak_factor
	dcs_content_tweak_factor	= dcs_content_tweak_factor.replace(tweak_factor1, tweak_factor)
	dcs_content					= dcs_content.replace(dcs_content_tweak_factor1, dcs_content_tweak_factor)
	# Get atomic_number_density:
	dcs_content_atomic_number_density	= dcs_content_sample.split("Angle of rotation and sample width (cm)\n-")[1]
	dcs_content_atomic_number_density	= dcs_content_atomic_number_density.split("Density atoms/")[0]
	atomic_number_density1				= dcs_content_atomic_number_density.split("          ")[0]
	#Change atomic_number_density.
	#~ atomic_number_density					= str(atomic_number_density)
	dcs_content_atomic_number_density1	= dcs_content_atomic_number_density
	dcs_content_atomic_number_density	= dcs_content_atomic_number_density.replace(atomic_number_density1, "%.3f" %(atomic_number_density))
	dcs_content					= dcs_content.replace(dcs_content_atomic_number_density1, dcs_content_atomic_number_density)

	print ("\nTweak Factor\t\t= " + tweak_factor + "\n")

	return dcs_content
	
#Start file loop.
print("\nStarting at "+time.asctime( time.localtime(time.time()) )+".\n")

total_gudrun_calls	= 0
for Sample in sample_sub_sets.keys():
	for RB_No in sample_sub_sets[Sample].keys():
		subset	= sample_sub_sets[Sample][RB_No]
		for file_set in subset:
			if Sample in ["VNb", "Instr", "CCR", "empty_can"]:
				pass
			else:
				total_gudrun_calls	+= 1
current_gudrun_call	= 0

for Sample in sample_sub_sets.keys():
	if Sample in ["VNb", "Instr", "CCR", "empty_can"]:
		pass
	
	else:
		for RB_No in sample_sub_sets[Sample].keys():
			if len(normalisations[RB_No]) < 1:
				break
			subset	= sample_sub_sets[Sample][RB_No]
			cycle	= sample_sub_set_cycles[Sample][RB_No]
			for file_set in subset:
				number_of_files		= len(file_set)
		
				# Navigate to data folder.
				data_file_directory	= data_directory + "/cycle_" + cycle
				os.chdir(data_file_directory)

				# Read log file:
				log_time	= []
				Time		= []
				Temp		= []
				for file in file_set:
					logfile = open("%s%i.log" %(instrument_tag, int(file)), "r")
					for line in logfile:
						log_time.append(line.split("\t")[0])
						if line.split("\t")[1] == "Sample_Bottom":
							Temp.append(float(line.split("\t")[-1]))
					logfile.close()
					
					for l in range(len(log_time)):
						log_time_value	= dt.datetime.strptime(log_time[l], "%Y-%m-%dT%H:%M:%S")
						difference		= log_time_value-t0
						Time.append(difference.total_seconds() / timedelta(hours=1).total_seconds())

				Time			= np.array(Time)

				times.append(Time.sum()/len(Time))
				time_err[0].append(times[-1] - np.min(Time))
				time_err[1].append(np.max(Time) - times[-1])

				Temp			= np.array(Temp)

				temperatures.append(Temp.sum()/len(Temp))
				temp_err[0].append(temperatures[-1] - np.min(Temp))
				temp_err[1].append(np.max(Temp) - temperatures[-1])
				
				# calculate water tweak factor and decide whether to iterate Gudrun for DCS match (by adding ethane)
				water_tweak		= float(tweak_fit_params[0]) + float(tweak_fit_params[1]) * temperatures[-1]
				if temperatures[-1] > 140:
					iterate_gudrun	= 0
				else:
					iterate_gudrun	= 1
				# Start values for thickness and tweak_factor:
				tweak_factor_save_to_file	= water_tweak
				tweak_factor				= tweak_factor_save_to_file		# 1/volume filling

				#Navigate to results folder.
				os.chdir(work_directory)
				os.chdir(results_directory)

				current_gudrun_call	+=	1
				print("---------------------\n\nRunning files %s/%s: %s scans %s.\n" %(current_gudrun_call, total_gudrun_calls, instrument_tag, file_set))
				print("Temperature =\t\t%.1f to %.1f\n" %(np.min(Temp), np.max(Temp)))
				print("water_tweak =\t\t%s\n" %(water_tweak))

				
				#Create file lists for Gudrun.
				normalisation_files="\n"
				for FILE in normalisations[RB_No]:
					normalisation_files = normalisation_files + "%s%s.raw          NORMALISATION data files\n" %(instrument_tag, FILE)
				Nr_of_files	= len(normalisations[RB_No])
				normalisation_files="\n%s  1          Number of  files and period number" %(Nr_of_files)+normalisation_files
					
				empty_instrument_files="\n"
				for FILE in empty_instruments[RB_No]:
					empty_instrument_files = empty_instrument_files + "%s%s.raw          NORMALISATION BACKGROUND data files\n" %(instrument_tag, FILE)
				Nr_of_files	= len(empty_instruments[RB_No])
				empty_instrument_files="%s  1          Number of  files and period number" %(Nr_of_files)+empty_instrument_files
					
				background_files="\n"
				for FILE in sample_environment[RB_No]:
					background_files = background_files + "%s%s.raw          SAMPLE BACKGROUND data files\n" %(instrument_tag, FILE)
				Nr_of_files	= len(sample_environment[RB_No])
				background_files="\n%s  1          Number of  files and period number" %(Nr_of_files)+background_files
				
				sample_files="\n"
				for FILE in file_set:
					sample_files = sample_files + "%s%s.raw          SAMPLE Sample data files\n" %(instrument_tag, FILE)
				sample_files="\n%s  1          Number of  files and period number" %(number_of_files)+sample_files
				
				container_files="\n"
				for FILE in file_set:
					container_files = container_files + "%s%s.raw          CONTAINER Can data files\n" %(instrument_tag, FILE)
				container_files="\n%s  1          Number of  files and period number" %(number_of_files)+container_files
					
				#Read gudrun dat file.
				f=open('gudrun_dcs.dat', 'r')
				dcs_content = f.read()
				f.close()

			##########          Data File Directory          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "INSTRUMENT          {"
				tab_end					= "\n}"
				dcs_content_instrument		= dcs_content.split(tab_start)[-1]
				dcs_content_instrument		= dcs_content_instrument.split("Gudrun input file directory:\n")[-1]
				dcs_data_file_directory1		= dcs_content_instrument.split("          Data file directory")[0]
				#~ dcs_instrument				= dcs_data_file_directory.split("NDX")[-1]
				#~ dcs_cycle					= dcs_cycle.split("\\")[0]
				#~ dcs_cycle					= dcs_data_file_directory.split("cycle_")[-1]
				#~ dcs_cycle					= dcs_cycle.split("\\")[0]
				
				# Change files to be analysed:
				dcs_data_file_directory		= "\\\\isis\\inst$\\NDX%s\\instrument\\data\\cycle_%s\\" %(instrument, str(cycle))
				dcs_content	= dcs_content.replace(dcs_data_file_directory1, dcs_data_file_directory)
				#~ print(time.asctime( time.localtime(time.time()) ) +"\tchanged directory.\n")

			##########          Normalisation          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "NORMALISATION          {\n"
				tab_end					= "\n}"
				dcs_content_normalisation	= dcs_content.split(tab_start)[-1]
				dcs_content_normalisation	= dcs_content_normalisation.split(tab_end)[0]
				dcs_normalisation_files		= dcs_content_normalisation.split("1          Force calculation of corrections?")[0]
				
				# Change files to be analysed:
				dcs_content	= dcs_content.replace(dcs_normalisation_files, normalisation_files+empty_instrument_files)
				#~ print(time.asctime( time.localtime(time.time()) ) +"\tchanged normalisation files.\n")

			##########          Sample Background          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "SAMPLE BACKGROUND          {\n"
				tab_end					= "\n}"
				dcs_content_background	= dcs_content.split(tab_start)[-1]
				dcs_background_files		= dcs_content_background.split(tab_end)[0]
				
				# Change files to be analysed:
				dcs_content	= dcs_content.replace(dcs_background_files, background_files)
				#~ print(time.asctime( time.localtime(time.time()) ) +"\tchanged background files.\n")

			##########          Sample          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "SAMPLE Sample          {\n"
				tab_end					= "\n}"
				dcs_content_sample			= dcs_content.split(tab_start)[-1]
				dcs_content_sample			= dcs_content_sample.split(tab_end)[0]
				dcs_sample_files			= dcs_content_sample.split("1          Force calculation of sample corrections?")[0]
				
				# Change files to be analysed:
				dcs_content	= dcs_content.replace(dcs_sample_files, sample_files)
				#~ print(time.asctime( time.localtime(time.time()) ) +"\tchanged sample files.\n")

			##########          Container          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "CONTAINER Can          {\n"
				tab_end					= "\n}"
				dcs_content_container		= dcs_content.split(tab_start)[-1]
				dcs_content_container		= dcs_content_container.split(tab_end)[0]
				dcs_container_files			= dcs_content_container.split("Ti  0  7.16          Composition")[0]
				
				# Change files to be analysed:
				dcs_content	= dcs_content.replace(dcs_sample_files, sample_files)
				#~ print(time.asctime( time.localtime(time.time()) ) +"\tchanged container files.\n")

			##########          Thickness          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "SAMPLE Sample          {\n"
				tab_end					= "\n}"
				dcs_content_sample			= dcs_content.split(tab_start)[-1]
				dcs_content_sample1		= dcs_content_sample.split(tab_end)[0]
				#Get thickness.
				dcs_content_thickness		= dcs_content_sample.split("SameAsBeam          Geometry")[1]
				dcs_content_thickness		= dcs_content_thickness.split("Upstream and downstream thicknesses ")[0]
				thickness1					= dcs_content_thickness.split("          ")[0][1:]
				#Change thickness.
				dcs_content_thickness1		= dcs_content_thickness
				dcs_content_thickness		= dcs_content_thickness.replace(thickness1, thickness)
				dcs_content_sample			= dcs_content_sample1.replace(dcs_content_thickness1, dcs_content_thickness)
				dcs_content					= dcs_content.replace(dcs_content_sample1, dcs_content_sample)
				#~ print(time.asctime( time.localtime(time.time()) ) +"\tchanged thickness.\n")
				
			##########          Run Gudrun          ##########
				#Start Gudrun loop.
				dcs_ch	= 0.05
				count	= 0

			##########          Sample Composition          ##########
				dcs_content, atomic_number_density, tweak_factor, ethane_water_ratio	= change_sample_composition(dcs_content, count, tweak_factor, suggested_tweak=1.)
				#~ print(time.asctime( time.localtime(time.time()) ) +"\tchanged composition.\n")
				
			##########          Tweak Factor & Density          ##########
				dcs_content					= change_tweak_and_density(dcs_content, atomic_number_density, water_tweak)	
				#~ print(time.asctime( time.localtime(time.time()) ) +"\tchanged tweak and density.\n")
				
				while True:
					print("\nIteration %i)\n" %(count+1))
					
					check_dcs	=0
					for dcsline in dcs_content.split("\n"):
						if "END" in dcsline:
							check_dcs	+=1
					if check_dcs > 1:
						print("\n\nscript interrupted\n\ncheck dcs file")
						break
							
					count 	= count + 1

					#Write dat file
					f	= open('gudrun_dcs.dat', 'w')
					f.write(dcs_content)
					f.close()
					
					#~ # check dat file contents
					#~ f		= open('gudrun_dcs.dat', 'r')
					#~ flines	= f.readlines()
					#~ f0		= open('gudrun_dcs_0_SANDALS.dat', 'r')
					#~ f0lines	= f0.readlines()
					#~ for l in range(len(flines)):
						#~ if flines[l] != f0lines[l]:
							#~ print("\nmismatch in line %i\n" %(l+1))
							#~ print(flines[l])
							#~ print(f0lines[l])

					#Run Gudrun
					print("Starting Gudrun at "+ time.asctime( time.localtime(time.time()) )+".")
					cmd		= "gudrun_dcs.exe"
					process	= subprocess.Popen(cmd,  creationflags=0x08000000)
					process.wait()
					print("Finished Gudrun at "+ time.asctime( time.localtime(time.time()) )+".")

					#Check if gud file exists
					test = "%s%s.gud" %(instrument_tag, file_set[0]) in os.listdir(".")
					if test == False:
						print("no results file")
						break

					#Read gud file
					f				= open("%s%s.gud" %(instrument_tag, file_set[0]), 'r')
					gud_content	= f.readlines()
					f.close()

					#Reads dcs level.
					dcs_line		= gud_content[dcs_line_number]
					
					if dcs_line[1:8]=='WARNING':
						number	= dcs_line[29:34]
						sign		= dcs_line[36:41]
						print(dcs_line[1:])
						if sign == 'ABOVE':
							dcs		= float(number)
							dcs_ch	= dcs*0.01
						else:
							dcs		= float(number)*-1.0
							dcs_ch	= dcs*0.01

					else:
						dcs_line	= dcs_line.rstrip('\n')
						print(dcs_line[1:]+".\n")
						dcs		= float(dcs_line[20:25])
						dcs_ch	= (dcs-100.0)*0.01

					if dcs_ch <= -1.0:
					    break
					
					elif (abs(dcs_ch) > 0.03) and (iterate_gudrun == 1):
						# Change tweak_factor and sample composition in dcs file:
						tweak_factor_save_to_file	= tweak_factor
						tweak_factor1				= tweak_factor
						for l in range(len(gud_content)):
							if "tweak factor" in gud_content[l]:
								suggested_tweak	= gud_content[l]
						suggested_tweak		= suggested_tweak.split("   ")[1]
						suggested_tweak		= suggested_tweak.split("\n")[0]
						suggested_tweak		= float(suggested_tweak)
						print ("\nSuggested Tweak Factor\t\t= %.2f\n" %(suggested_tweak))
						if suggested_tweak == float(tweak_factor):
							break

						dcs_content, atomic_number_density, tweak_factor, ethane_water_ratio	= change_sample_composition(dcs_content, count, tweak_factor, suggested_tweak)
						dcs_content	= change_tweak_and_density(dcs_content, atomic_number_density, tweak_factor)	
					
					else:
						break
						
				os.chdir("..")
				if test == True and dcs_ch > -1.0 and input["note"][i]=="":
					file_list	= ""
					for file in file_set:
						file_list	= file_list + "_" + str(file)
					print("Satisfactory DCS level achieved.\n%i Iterations\nTotal Thickness\t= %.4f cm\nTweak Factor\t= %.2f\n" %(count, 2*float(thickness1.split("  ")[0]), float(tweak_factor_save_to_file)))
					output.append(	    "%s\t" %(cycle) 
									+ "%s\t" %(RB_No) 
									+ "%s\t" %(Sample) 
									+ "%s\t" %(file_list) 
									+ "%.6f\t" %(float(thickness_save_to_file)) 
									+ "%.6f\t" %(float(tweak_factor_save_to_file)) 
									+ "%.6f\t" %(atomic_number_density) 
									+ "%.6f\t" %(ethane_water_ratio) 
									+ "%.3f\t" %(water_tweak) 
									+ "%.5f\t" %(times[current_gudrun_call-1]) 
									+ "%.5f\t" %(time_err[0][current_gudrun_call-1]) 
									+ "%.5f\t" %(time_err[1][current_gudrun_call-1]) 
									+ "%.5f\t" %(temperatures[current_gudrun_call-1]) 
									+ "%.5f\t" %(temp_err[0][current_gudrun_call-1]) 
									+ "%.5f\n" %(temp_err[1][current_gudrun_call-1])
									)
					# write results to file
					f	= open("results_%s.txt" %(analysis), 'w')
					f.writelines(output)
					f.close()
				elif test == False:
					issues +=1
					print("File error for %s scans %s.\n" %(instrument_tag, file_set))
					# write message to file
					analysis_issues_output.append("%s\tNo Gudrun output file.\n" %(file_set))
				else:
					issues +=1
					print("Satisfactory DCS level will not be achieved.\n")
					# write message to file
					analysis_issues_output.append("%s\tSatisfactory DCS level will not be achieved.\n"%(file_set))
				f1						= open("analysis_issues_%s.txt" %(analysis), 'w')
				f1.writelines(analysis_issues_output)
				f1.close()

				dcs_sample_files	= sample_files

print("---------------------\n\nAll files completed.\n")
print("---------------------\n\n%i files not analysed.\n" %(issues))
print("Finished at "+time.asctime( time.localtime(time.time()) )+".\n")
