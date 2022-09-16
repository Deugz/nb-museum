import subprocess
import os
import time
import datetime as dt
from datetime import timedelta
import numpy as np

''' 
--------------------------------------------------------------------------------------------------------------
	2017: Sabrina Gaertner
    2019: Updated by Vincent Deguin
--------------------------------------------------------------------------------------------------------------
This script runs Gudrun for a number of specified files in the <analysis>.csv file.
The tweak_factor or sample thickness can be changed each time until the DCS level is within specified range of expected level.
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
		f) Save the resulting file as BOTH .xls/.xlsx AND .csv (top folder)
		   (the csv is read by the Python script, but any formatting and automated filling, 
		   which you may need for future reference will only work in .xls/.xlsx format).
	5) Check the entries in <analysis> and <instrument> are up-to-date.
    6) Check data directory
--------------------------------------------------------------------------------------------------------------
'''

# Identification tags for filenames:
analysis				= "D2O_FIRST_TRY_analysis_08_05_19"
instrument			= "NIMROD"			# "SANDALS" or "NIMROD"

# Fit tweak factor or sample thickness?
fit_tweak			= 1			# 0=no, 1=yes
fit_thickness		= 0			# 0=no, 1=yes

# number of files to be averaged:
N_average			= 500

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
work_directory		= os.getcwd()
results_directory	= os.getcwd() + "/Gudrun_Results"
data_directory		= "../Data_Practise/" 
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

# Start values for thickness and tweak_factor:
tweak_factor_save_to_file	= 4.97
tweak_factor				= tweak_factor_save_to_file		# 1/volume filling
thickness_save_to_file		= 0.2
thickness					= thickness_save_to_file/2.		# half of sample thickness (cm)
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
	elif input["Bin"][i]:
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
output.append("#fitted thickness: %i\n#fitted tweak_factor: %i\n" %(fit_thickness, fit_tweak))
output.append("cycle\tRB_No\tsample\tfiles\ttotal_thickness\ttweak_factor\ttimes\ttime_err_neg\ttime_err_pos\ttemperatures\ttemp_err_neg\ttemp_err_pos\n")
output.append("#\t\t(cm)\t\t(h)\t(h)\t(h)\n")

analysis_issues_output	= []
issues					= 0


#Start file loop.
print("\nStarting at "+time.asctime( time.localtime(time.time()) )+".\n")

total_gudrun_calls	= 0
for Sample in sample_sub_sets.keys():
	for RB_No in sample_sub_sets[Sample].keys():
		subset	= sample_sub_sets[Sample][RB_No]
		for file_set in subset:
			if Sample in ["VNb", "Instr", "Bin", "empty_can"]:
				pass
			else:
				total_gudrun_calls	+= 1
current_gudrun_call	= 0

for Sample in sample_sub_sets.keys():
	if Sample in ["VNb", "Instr", "Bin", "empty_can"]:
		pass
	
	else:
		for RB_No in sample_sub_sets[Sample].keys():
			if len(normalisations[RB_No]) < 1:
				break
			subset	= sample_sub_sets[Sample][RB_No]
			cycle	= sample_sub_set_cycles[Sample][RB_No]
			for file_set in subset:
				number_of_files		=	len(file_set)
		
				# Navigate to data folder.
				os.chdir(data_directory)

				# Read log file:
				log_time	= []
				Time		= []
				Temp		= []
				for file in file_set:
					logfile = open("%s%i.log" %(instrument_tag, int(file)), "r")
					for line in logfile:
						log_time.append(line.split("\t")[0])
						if line.split("\t")[1] == "Sample":
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

				#Navigate to results folder.
				os.chdir(work_directory)
				os.chdir(results_directory)

				current_gudrun_call	+=	1
				print("---------------------\n\nRunning files %s/%s: %s scans %s.\n" %(current_gudrun_call, total_gudrun_calls, instrument_tag, file_set))

				
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
				dcs_data_file_directory		= data_directory.replace("/", '\\')
				dcs_content	= dcs_content.replace(dcs_data_file_directory1, dcs_data_file_directory)

			##########          Normalisation          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "NORMALISATION          {\n"
				tab_end					= "\n}"
				dcs_content_normalisation	= dcs_content.split(tab_start)[-1]
				dcs_content_normalisation	= dcs_content_normalisation.split(tab_end)[0]
				dcs_normalisation_files		= dcs_content_normalisation.split("1          Force calculation of corrections?")[0]
				
				# Change files to be analysed:
				dcs_content	= dcs_content.replace(dcs_normalisation_files, normalisation_files+empty_instrument_files)

			##########          Sample Background          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "SAMPLE BACKGROUND          {\n"
				tab_end					= "\n}"
				dcs_content_background	= dcs_content.split(tab_start)[-1]
				dcs_background_files		= dcs_content_background.split(tab_end)[0]
				
				# Change files to be analysed:
				dcs_content	= dcs_content.replace(dcs_background_files, background_files)

			##########          Sample          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "SAMPLE Sample          {\n"
				tab_end					= "\n}"
				dcs_content_sample			= dcs_content.split(tab_start)[-1]
				dcs_content_sample			= dcs_content_sample.split(tab_end)[0]
				dcs_sample_files			= dcs_content_sample.split("1          Force calculation of sample corrections?")[0]
				
				# Change files to be analysed:
				dcs_content	= dcs_content.replace(dcs_sample_files, sample_files)

			##########          Container          ##########
				# Get entries in dcs file that refer to the right tab:
				tab_start					= "CONTAINER Can          {\n"
				tab_end					= "\n}"
				dcs_content_container		= dcs_content.split(tab_start)[-1]
				dcs_content_container		= dcs_content_container.split(tab_end)[0]
				dcs_container_files			= dcs_content_container.split("Ti  0  7.16          Composition")[0]
				
				# Change files to be analysed:
				dcs_content	= dcs_content.replace(dcs_sample_files, sample_files)

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
				
			##########          Tweak Factor          ##########
				# Get tweak_factor:
				dcs_content_tweak_factor	= dcs_content_sample.split("Total cross section source")[1]
				dcs_content_tweak_factor	= dcs_content_tweak_factor.split("0          Top hat width")[0]
				tweak_factor1				= dcs_content_tweak_factor.split("          ")[0][1:]
				#Change tweak_factor.
				tweak_factor				= str(tweak_factor)
				dcs_content_tweak_factor1	= dcs_content_tweak_factor
				dcs_content_tweak_factor	= dcs_content_tweak_factor.replace(tweak_factor1, tweak_factor)
				dcs_content					= dcs_content.replace(dcs_content_tweak_factor1, dcs_content_tweak_factor)

				#~ break	
			##########          Run Gudrun          ##########
				#Start Gudrun loop.
				dcs_ch	= 0.05
				count	= 0
				while abs(dcs_ch) > 0.03:
					count 	= count + 1
					print("Total Thickness\t= %.4f cm" %(2 * float(thickness.split("  ")[0])))
					print ("Tweak Factor\t= %.2f" %(float(tweak_factor + "\n")))

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
					f			= open("%s%s.gud" %(instrument_tag, file_set[0]), 'r')
					gud_content	= f.readlines()
					f.close()

					#Reads dcs level.
					dcs_line	= gud_content[dcs_line_number]
					
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
					
					elif fit_tweak == 1 and fit_thickness == 0:
						# Change tweak_factor in dcs file:
						tweak_factor_save_to_file	= tweak_factor
						tweak_factor1			= tweak_factor
						for l in range(len(gud_content)):
							if "tweak factor" in gud_content[l]:
								tweak_factor	= gud_content[l]
							else:
								pass
						tweak_factor			= tweak_factor.split("   ")[1]
						tweak_factor			= tweak_factor.split("\n")[0]
						dcs_content_tweak_factor1	= dcs_content_tweak_factor
						dcs_content_tweak_factor	= dcs_content_tweak_factor.replace(tweak_factor1, tweak_factor)
						dcs_content			= dcs_content.replace(dcs_content_tweak_factor1, dcs_content_tweak_factor)

					elif fit_tweak == 0 and fit_thickness == 1:
						# Change thickness in dcs file:
						thickness_save_to_file	= 2*float(thickness.split("  ")[0])
						thickness1				= thickness
						for l in range(len(gud_content)):
							if "tweak factor" in gud_content[l]:
								suggested_tweak	= gud_content[l]
							else:
								pass
						suggested_tweak		= suggested_tweak.split("    ")[1]
						suggested_tweak		= suggested_tweak.split("\n")[0]
						suggested_tweak		= float(suggested_tweak)
						factor					= float(tweak_factor)/float(suggested_tweak)
						thickness				= thickness.split("  ")[0]
						thickness				= float(thickness)*factor
						thickness				= str(thickness) + "  " + str(thickness)
						dcs_content_thickness1	= dcs_content_thickness
						dcs_content_thickness	= dcs_content_thickness.replace(thickness1, thickness)
						dcs_content				= dcs_content.replace(dcs_content_thickness1, dcs_content_thickness)
					
					elif fit_tweak == 0 and fit_thickness == 0:
						break

					elif fit_tweak == 1 and fit_thickness == 1:
						print("\n\n\n====================\n\n\nPlease choose only tweak factor OR thickness fitting!\n\n\n====================\n\n\n")
						break

				os.chdir("..")
				if test == True and dcs_ch > -1.0 and input["note"][i]=="":
					file_list	= ""
					for file in file_set:
						file_list	= file_list + "_" + str(file)
					print("Satisfactory DCS level achieved.\n%i Iterations\nTotal Thickness\t= %.4f cm\nTweak Factor\t= %.2f\n" %(count, 2*float(thickness1.split("  ")[0]), float(tweak_factor_save_to_file)))
					output.append("%s\t%s\t%s\t%s\t%.6f\t%.3f\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f\n" %(cycle, RB_No, Sample, file_list, float(thickness_save_to_file), float(tweak_factor_save_to_file), times[current_gudrun_call-1], time_err[0][current_gudrun_call-1], time_err[1][current_gudrun_call-1], temperatures[current_gudrun_call-1], temp_err[0][current_gudrun_call-1], temp_err[1][current_gudrun_call-1]))
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
