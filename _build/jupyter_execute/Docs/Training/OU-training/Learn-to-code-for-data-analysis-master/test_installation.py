#!/usr/bin/env python
# coding: utf-8

# # Software installation test
# 
# This Jupyter notebook is for The Open University's _Learn to code for data analysis_ course.
# It checks whether your software installation is working as expected.
# 
# To do that, you must open this notebook from within the Jupyter app in Anaconda 
# or by using a cloud service like CoCalc or Microsoft Azure. 
# 
# Then, in the menu above, click on 'Cell' and then on 'Run all'.
# This will execute the code below. (The code will be explained in the course.)
# 
# After a while you should see some text stating which version of pandas
# (the data analysis software we will be using) you have installed, 
# and after another moment you should see a graph with two dots plotted on it.
# If you are using a cloud service to run Jupyter notebooks,
# it will take longer for the text and graph to appear.
# In Azure you may get a warning that the font cache for graph labels is being built.
# 
# ## Anaconda
# 
# If you're using Anaconda, if the pandas version displayed is 0.20 or higher and you don't get any error messages, 
# then all's well and you can close this notebook (menu 'File', option 'Close and Halt') 
# and then delete the notebook from your disk if you wish.
# 
# If there is an error message saying you don't have Python 3, 
# or if the pandas version displayed is below 0.20, 
# then one of the following has probably happened: 
# 
# - you installed the wrong version of Anaconda;
# - you installed the wrong variant of Anaconda (there are two variants, for Python 2 and Python 3, of the same version of Anaconda); 
# - during the installation you decided to keep your existing Python installation. 
# 
# To see which software versions you have installed, 
# click on the 'Help' menu above, and then on the 'About' option. 
# You should have the notebook server version 5.0 or higher, 
# Python version 3.5 or higher, and IPython version 6.1 or higher. 
# 
# ## CoCalc and Microsoft Azure
# 
# If you're using one of these cloud services and if there are no error messages, 
# then all's well and you can close this notebook and delete it from 
# your project (CoCalc) or library (Azure) if you wish. 
# To close a notebook in CoCalc, click x on the tab at the top. 
# To close a notebook in Azure, select menu 'File', option 'Close and Halt'.
# 
# If you get an error that you don't have Python 3, then click on the 'Kernel' menu above, 
# select the 'Change kernel' option, and finally select one of the 'Python 3' options in the menu. 
# You will see some messages on the top right side whilst the kernel
# (the software that runs the notebook) is being changed. 
# Once the messages disappear, you can click again on 'Run all' in the 'Cell' menu.

# In[1]:


import warnings
warnings.simplefilter('ignore', FutureWarning)

from pandas import *
print('Your pandas version is', pandas.__version__)

if 1 / 2 == 0:
    print('Error: you are not running Python 3')
    
df = DataFrame(data=[[1,2], [2,1]], columns=['x','y'])

get_ipython().run_line_magic('matplotlib', 'inline')
df.plot('x', 'y', kind='scatter')

from scipy.stats import spearmanr

