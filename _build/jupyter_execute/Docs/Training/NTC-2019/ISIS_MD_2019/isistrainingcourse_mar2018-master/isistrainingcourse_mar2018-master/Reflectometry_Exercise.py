#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np 
from falass import readwrite, job, sld, reflect, compare


# # ISIS Neutron Training Course
# ## MD-based analysis of neutron reflectometry
# 
# #### Andrew R. McCluskey 
# ##### University of Bath/Diamond Light Source - arm61@bath.ac.uk
# 
# 2018-03-08
# 
# In this exercise, you will analyse neutron reflectometry data using a molecular dynamics simulation. The system that was studied is a DSPC monolayer, with five contrasts being measured:
# 
# - d$_{83}$-DSPC in ACMW
# - d$_{70}$-DSPC in ACMW
# - d$_{83}$-DSPC in D$_2$O
# - d$_{70}$-DSPC in D$_2$O
# - h-DSPC in D$_2$O
# 
# The aim of this exercise is to understand how reflectometry experiments can be analysed using molecular dynamics simulation, and putting this into action by identifying the comparing two simulations at different areas per molecule to identify which matches more closely with the experimental data. This will involve using the python package falass.[1] falass is capable of reading in molecular dynamics simulation trajectory (e.g. the atomic positions at a series of simulation timesteps) and returning a reflectometry profile. Full documentation for falass is available at https://readthedocs.org/projects/falass/.
# 
# The first thing to do with falass is to read in the experimental data, these files are all in the 'data' directory, and can be read in with the 
# 
# ```
# readwrite.Files(datfile='filepath')
# ```
# 
# command. 

# In[24]:


files_d83acmw = readwrite.Files(datfile='data/d83acmw.dat')
files_d70acmw = readwrite.Files(datfile='data/d70acmw.dat')
files_d83d2o = readwrite.Files(datfile='data/d83d2o.dat') 
files_d70d2o = readwrite.Files(datfile='data/d70d2o.dat')
files_hd2o = readwrite.Files(datfile='data/hd2o.dat')


# These .dat files are three column comma separated files consisting of information about q, reflected intensity and an uncertainty in reflected intensity.

# In[25]:


cat data/d83acmw.dat


# The above command simply defined the datfile in the files class, these now must be read into computer memory.

# In[26]:


files_d70acmw.read_dat()
files_d83acmw.read_dat()
files_d70d2o.read_dat()
files_d83d2o.read_dat()
files_hd2o.read_dat()


# We can also plot this data to check that the right files have been read in. 

# In[27]:


d70acmw_data = files_d70acmw.plot_dat(rq4=False)
d70acmw_data.show()
d83acmw_data = files_d83acmw.plot_dat(rq4=False)
d83acmw_data.show()
d70d2o_data = files_d70d2o.plot_dat(rq4=False)
d70d2o_data.show()
d83d2o_data = files_d83d2o.plot_dat(rq4=False)
d83d2o_data.show()
hd2o_data = files_hd2o.plot_dat(rq4=False)
hd2o_data.show()


# In[18]:


files_d13acmw.lgtfile = 'data/d13acmw.lgt'


# In[19]:


files_d13acmw.read_lgt()


# [1] *falass*, Andrew R. McCluskey, (http://people.bath.ac.uk/arm61/falass/)

# In[52]:


a = np.tan(10/500)
b = np.rad2deg(a)
print(b)


# In[ ]:




