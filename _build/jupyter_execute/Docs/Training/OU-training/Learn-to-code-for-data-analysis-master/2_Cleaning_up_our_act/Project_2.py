#!/usr/bin/env python
# coding: utf-8

# # Project 2:  Holiday weather
# 
# by Rob Griffiths, 11 September 2015, updated 11 April, 18 October and 20 December 2017, 5 August 2020
# 
# This is the project notebook for the second part of The Open University's _Learn to code for Data Analysis_ course.
# 
# There is nothing I like better than taking a holiday. In the winter I like to have a two week break in a country where I can be guaranteed sunny dry days. In the summer I like to have two weeks off relaxing in my garden in London. However I'm often disappointed because I pick a fortnight when the weather is dull and it rains. So in this project I am going to use the historic weather data from the Weather Underground for London to try to predict two good weather weeks to take off as holiday next summer. Of course the weather in the summer of 2016 may be very different to 2014 but it should give me some indication of when would be a good time to take a summer break.
# 
# ## Getting the data
# 
# Weather Underground keeps historical weather data collected in many airports around the world. Right-click on the following URL and choose 'Open Link in New Window' (or similar, depending on your browser):
# 
# http://www.wunderground.com/history
# 
# _(The following instructions were correct as of 2017. Wunderground has since changed its data provision.)_
# 
# When the new page opens start typing 'LHR' in the 'Location' input box and when the pop up menu comes up with the option 'LHR, United Kingdom' select it and then click on 'Submit'. 
# 
# When the next page opens with London Heathrow data, click on the 'Custom' tab and select the time period From: 1 January 2014 to: 31 December 2014 and then click on 'Get History'. The data for that year should then be displayed further down the page. 
# 
# You can copy each month's data directly from the browser to a text editor like Notepad or TextEdit, to obtain a single file with as many months as you wish.
# 
# Weather Underground has changed in the past the way it provides data and may do so again in the future. 
# I have therefore collated the whole 2014 data in the provided 'London_2014.csv' file. 
# 
# Now load the CSV file into a dataframe making sure that any extra spaces are skipped:

# In[1]:


import warnings
warnings.simplefilter('ignore', FutureWarning)

from pandas import *
from datetime import datetime

london = read_csv('London_2014.csv', skipinitialspace=True)


# ## Cleaning the data
# First we need to clean up the data. I'm not going to make use of `'WindDirDegrees'` in my analysis, but you might in yours so we'll rename `'WindDirDegrees< br />'` to `'WindDirDegrees'`. 

# In[2]:


london = london.rename(columns={'WindDirDegrees<br />' : 'WindDirDegrees'})


# remove the  `< br />`  html line breaks from the values in the `'WindDirDegrees'` column. 

# In[3]:


london['WindDirDegrees'] = london['WindDirDegrees'].str.rstrip('<br />')


# and change the values in the `'WindDirDegrees'` column to `float64`:

# In[4]:


london['WindDirDegrees'] = london['WindDirDegrees'].astype('float64')   


# We definitely need to change the values in the `'GMT'` column into values of the `datetime64`  date type.

# In[5]:


london['GMT'] = to_datetime(london['GMT'])


# We also need to change the index from the default to the `datetime64` values in the `'GMT'` column so that it is easier to pull out rows between particular dates and display more meaningful graphs: 

# In[6]:


london.index = london['GMT']


# ## Finding a summer break
# 
# According to meteorologists, summer extends for the whole months of June, July, and August in the northern hemisphere and the whole months of December, January, and February in the southern hemisphere. So as I'm in the northern hemisphere I'm going to create a dataframe that holds just those months using the `datetime` index, like this:

# In[7]:


summer = london.loc[datetime(2014,6,1) : datetime(2014,8,31)]


# I now look for the days with warm temperatures.

# In[8]:


summer[summer['Mean TemperatureC'] >= 25]


# Summer 2014 was rather cool in London: there are no days with temperatures of 25 Celsius or higher. Best to see a graph of the temperature and look for the warmest period.
# 
# So next we tell Jupyter to display any graph created inside this notebook:

# In[9]:


get_ipython().run_line_magic('matplotlib', 'inline')


# Now let's plot the `'Mean TemperatureC'` for the summer:

# In[10]:


summer['Mean TemperatureC'].plot(grid=True, figsize=(10,5))


# Well looking at the graph the second half of July looks good for mean temperatures over 20 degrees C so let's also put precipitation on the graph too:

# In[11]:


summer[['Mean TemperatureC', 'Precipitationmm']].plot(grid=True, figsize=(10,5))


# The second half of July is still looking good, with just a couple of peaks showing heavy rain. Let's have a closer look by just plotting mean temperature and precipitation for July.  

# In[12]:


july = summer.loc[datetime(2014,7,1) : datetime(2014,7,31)]
july[['Mean TemperatureC', 'Precipitationmm']].plot(grid=True, figsize=(10,5))


# Yes, second half of July looks pretty good, just two days that have significant rain, the 25th and the 28th and just one day when the mean temperature drops below 20 degrees, also the 28th.

# ## Conclusions
# 
# The graphs have shown the volatility of a British summer, but a couple of weeks were found when the weather wasn't too bad in 2014. Of course this is no guarantee that the weather pattern will repeat itself in future years. To make a sensible prediction we would need to analyse the summers for many more years. By the time you have finished this course you should be able to do that.
