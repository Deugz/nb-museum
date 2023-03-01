#!/usr/bin/env python
# coding: utf-8

# # Exercise notebook 3: Transforming and Combining Data
# 
# This Jupyter notebook is for Part 3 of The Open University's _Learn to code for Data Analysis_ course.
# 
# This notebook has all code examples and coding exercises. Remember to start by running the code in this notebook. You will need to add a code cell below each task to complete it.
# 
# You'll come across steps in the course directing you to this notebook. Once you've done each exercise, go back to the corresponding step and mark it as complete.

# In[1]:


import warnings
warnings.simplefilter('ignore', FutureWarning)

from pandas import *


# ## Exercise 1: Creating the data

# Dataframes can be constructed from scratch as follows.

# In[2]:


headings = ['Country', 'GDP (US$)']
table = [
  ['UK', 2678454886796.7],    # 1st row
  ['USA', 16768100000000.0],  # 2nd row
  ['China', 9240270452047.0], # and so on...
  ['Brazil', 2245673032353.8],
  ['South Africa', 366057913367.1]
]
gdp = DataFrame(columns=headings, data=table)
gdp


# And similarly for the life expectancy of those born in 2013...

# In[3]:


headings = ['Country name', 'Life expectancy (years)']
table = [
  ['China', 75],
  ['Russia', 71],  
  ['United States', 79],
  ['India', 66],
  ['United Kingdom', 81]
]
life = DataFrame(columns=headings, data=table)
life


# ### Task
# 
# Create a dataframe with all five BRICS countries and their population, in thousands of inhabitants, in 2013. The values (given in the first exercise notebook) are: Brazil 200362, Russian Federation 142834, India 1252140, China 1393337, South Africa 52776.

# **Now go back to the course.**

# ## Exercise 2: Defining functions
# 
# The following function, written in two different ways, rounds a number to the nearest million. It calls the Python function `round()` which rounds a decimal number to the nearest integer. If two integers are equally near, it rounds to the even integer.

# In[4]:


def roundToMillions (value):
    result = round(value / 1000000)
    return result


# In[5]:


def roundToMillions (value):
    return round(value / 1000000)


# To test a function, write expressions that check for various argument values whether the function returns the expected value in each case.

# In[6]:


roundToMillions(4567890.1) == 5


# In[7]:


roundToMillions(0) == 0  # always test with zero...


# In[8]:


roundToMillions(-1) == 0 # ...and negative numbers


# In[9]:


roundToMillions(1499999) == 1 # test rounding to the nearest


# The next function converts US dollars to British pounds.

# In[10]:


def usdToGBP (usd):
    return usd / 1.564768 # average rate during 2013 

usdToGBP(0) == 0


# In[11]:


usdToGBP(1.564768) == 1


# In[12]:


usdToGBP(-1) < 0


# ### Tasks
# 
# 1. Define a few more test cases for both functions.
# - Why can't you use `roundToMillions()` to round the population to millions of inhabitants? Write a new function and test it. **You need to write this function in preparation for Exercise 4.**
# - Write a function to convert US dollars to your local currency. If your local currency is USD or GBP, convert to Euros. Look up online what was the average exchange rate in 2013.

# **Now go back to the course.**

# ## Exercise 3: What if...?
# 
# The next function uses the full form of the conditional statement to expand the abbreviated country names UK and USA and leave other names unchanged.

# In[13]:


def expandCountry (name):
    if name == 'UK':
        return 'United Kingdom'
    elif name == 'USA':
        return 'United States'
    else:
        return name

expandCountry('India') == 'India'


# Here is the same function, written differently, using the simplest form of the conditional statement, without the `elif` and `else` parts.

# In[14]:


def expandCountry (name):
    if name == 'UK':
        name = 'United Kingdom'
    if name == 'USA':
        name = 'United States'
    return name


# ### Tasks
# 
# 1. Write more tests.
# - Explain why the second version of the function works. Note how the code is indented.
# - Extend both versions to expand 'St. Lucia' to 'Saint Lucia'.
# - Write a function to translate some country names from their original language to English, e.g. 'Brasil' to 'Brazil', 'España' to 'Spain' and 'Deutschland' to 'Germany'.
# - Can you think of a different way of expanding abbreviated country names? You're not expected to write any code. Hint: this is a course about data tables.

# **Now go back to the course.**

# ## Exercise 4: Applying functions
# 
# A one-argument function can be applied to each cell in a column, in order to obtain a new column with the converted values.

# In[15]:


gdp['Country name'] = gdp['Country'].apply(expandCountry)
gdp


# Given that `apply()` is a column method that returns a column, it can be **chained**, to apply several conversions in one go.

# In[16]:


gdp['GDP (£m)'] = gdp['GDP (US$)'].apply(usdToGBP).apply(roundToMillions)
gdp


# Applying the conversion functions in a different order will lead to a different result.

# In[17]:


gdp['GDP (US$)'].apply(roundToMillions).apply(usdToGBP).apply(round)


# The original columns can be discarded.

# In[18]:


headings = ['Country name', 'GDP (£m)']
gdp = gdp[headings]
gdp


# ### Task
# 
# Take the dataframe you created for Exercise 1, and apply to its population column the rounding function you wrote in Exercise 2.

# **Now go back to the course.**

# ## Exercise 5: Joining left, right and centre
# 
# At this point, both tables have a common column, 'Country name', with fully expanded country names.

# In[19]:


life


# In[20]:


gdp


# A **left join** takes the rows of the left table and adds the columns of the right table. 

# In[21]:


merge(gdp, life, on='Country name', how='left')


# A **right join** takes the rows from the right table, and adds the columns of the left table.

# In[22]:


merge(gdp, life, on='Country name', how='right')


# An **outer join** takes the union of the rows, i.e. it has all the rows of the left and right joins.

# In[23]:


merge(gdp, life, on='Country name', how='outer')


# An **inner join** takes the intersection of the rows (i.e. the common rows) of the left and right joins.

# In[24]:


gdpVsLife = merge(gdp, life, on='Country name', how='inner')
gdpVsLife


# ### Task
# 
# Join your population dataframe (from Exercise 4) with `gdpVsLife`, in four different ways, and note the differences.

# **Now go back to the course.**

# ## Exercise 6: Constant variables
# 
# Constants are used to represent fixed values (e.g. strings and numbers) that occur frequently in a program. Constant names are conventionally written in uppercase, with underscores to separate multiple words.

# In[25]:


GDP_USD = 'GDP (US$)'
GDP_GBP = 'GDP (£m)'
GDP_USD


# ### Task
# 
# Look through the code you wrote so far, and rewrite it using constants, when appropriate.

# **Now go back to the course.**

# ## Exercise 7: Getting real
# 
# It is possible to directly download data from the World Bank, for a particular time period and indicator, like the GDP in current US dollars. The indicator name is given in the URL of the webpage about the dataset.
# 
# Getting the data directly from the World Bank only works with Anaconda (or a paid CoCalc account) and requires an Internet connection. It can take some time to download the data, depending on the speed of your connection and the load on the World Bank server. Moreover, the World Bank occasionally changes the layout of the data, which could break the code in the rest of this notebook. 
# 
# To avoid such problems I have saved the World Bank data into CSV files. The data is in a column with the same name as the indicator. Hence I declare the indicator names as constants, to be used later when processing the dataframe.

# In[26]:


GDP_INDICATOR = 'NY.GDP.MKTP.CD'
gdpReset = read_csv('WB GDP 2013.csv')

LIFE_INDICATOR = 'SP.DYN.LE00.IN'
lifeReset = read_csv('WB LE 2013.csv')


# The CSV files were obtained in two steps, which are shown next in commented code because we already have the CSV files. 
# 
# First the data was obtained directly from the World Bank using a particular function in pandas, and indicating the desired indicator and time period. Note that you may have to install the `pandas_datareader` module, using Anaconda Navigator.

# In[27]:


# if pandas.__version__.startswith('0.23'):
#     # this solves an incompatibility between pandas 0.23 and datareader 0.6
#     # taken from https://stackoverflow.com/questions/50394873/
#     core.common.is_list_like = api.types.is_list_like

# from pandas_datareader.wb import download

# YEAR = 2013
# gdpWB = download(indicator=GDP_INDICATOR, country='all', start=YEAR, end=YEAR)
# lifeWB = download(indicator=LIFE_INDICATOR, country='all', start=YEAR, end=YEAR)
# lifeWB.head()


# The downloaded dataframe has descriptive row names instead of the usual 0, 1, 2, etc. In other words, the dataframe's index is given by the country and year instead of integers. Hence the second step was to reset the index. 

# In[28]:


# gdpReset = gdpWB.reset_index()
# lifeReset = lifeWB.reset_index()


# Resetting the index put the dataframes into the usual form, which was saved to CSV files. 

# In[29]:


lifeReset.head()


# ### Tasks
# 
# 1. Create a data frame with the World Bank's data on population, using the CSV file provided. **This dataframe will be used in the remaining exercises.**
# - If you're using Anaconda, uncomment the code above and run it to check that you can get the GDP and life expectancy data directly from the World Bank. **Don't forget to afterwards comment again the code.**
# - If you have extra time, you can alternatively obtain the population data directly from the World Bank: go to their [data page](http://data.worldbank.org/), search for population, select the total population indicator, note its name in the URL, copy the commented code above and adapt it to get the data and reset its index. Note that the World Bank may have changed its data format since this was written and therefore you may have to do extra steps to get a dataframe in the same shape as the CSV file we provide, with three columns for country name, year and population.

# **Now go back to the course.**

# ## Exercise 8: Cleaning up
# 
# The expression `frame[m:n]` represents a dataframe with only row `m` to row `n-1` (or until the end if `n` is omitted) of `frame`.

# In[30]:


lifeReset[0:3]


# In[31]:


lifeReset[240:]


# The first rows of World Bank dataframes are aggregated data for country groups, and are thus discarded. There were 34 country groups when I generated the CSV files, but the World Bank sometimes adds or removes groups. Therefore, if you obtained the data directly from the World Bank, you may need to discard more or fewer than 34 rows to get a dataframe that starts with Afghanistan.

# In[32]:


gdpCountries = gdpReset[34:]
lifeCountries = lifeReset[34:]
gdpCountries.head()


# Rows with missing data are dropped.

# In[33]:


gdpData = gdpCountries.dropna()
lifeData = lifeCountries.dropna()
gdpData.head()


# The year column is discarded.

# In[34]:


COUNTRY = 'country'
headings = [COUNTRY, GDP_INDICATOR]
gdpClean = gdpData[headings]
headings = [COUNTRY, LIFE_INDICATOR]
lifeClean = lifeData[headings]
lifeClean.head()


# ### Task
# 
# Clean the population dataframe you created in Exercise 7.
# 
# If in Exercise 7 you chose to directly get the population data from the World Bank instead of using the provided CSV file, you may need to remove more (or fewer) than 34 rows at the start of the dataframe due to changes done by the World Bank to its data reporting.

# **Now go back to the course.**

# ## Exercise 9: Joining and transforming
# 
# The two dataframes can now be merged with an inner join.

# In[35]:


gdpVsLifeAll = merge(gdpClean, lifeClean, on=COUNTRY, how='inner')
gdpVsLifeAll.head()


# The dollars are converted to million pounds.

# In[36]:


GDP = 'GDP (£m)'
column = gdpVsLifeAll[GDP_INDICATOR]
gdpVsLifeAll[GDP] = column.apply(usdToGBP).apply(roundToMillions)
gdpVsLifeAll.head()


# The life expectancy is rounded, by applying the `round()` function.

# In[37]:


LIFE = 'Life expectancy (years)'
gdpVsLifeAll[LIFE] = gdpVsLifeAll[LIFE_INDICATOR].apply(round)
gdpVsLifeAll.head()


# The original GDP and life expectancy columns are dropped.

# In[38]:


headings = [COUNTRY, GDP, LIFE]
gdpVsLifeClean = gdpVsLifeAll[headings]
gdpVsLifeClean.head()


# ### Tasks
# 
# 1. Merge `gdpVsLifeClean` with the population dataframe obtained in the previous exercise. 
# - Round the population value to the nearest million.
# - Remove the original population column.

# **Now go back to the course.**

# ## Exercise 10: Correlation
# 
# The Spearman rank correlation coefficient between GDP and life expectancy, and the corresponding p-value are calculated as follows.

# In[39]:


from scipy.stats import spearmanr

gdpColumn = gdpVsLifeClean[GDP]
lifeColumn = gdpVsLifeClean[LIFE]
(correlation, pValue) = spearmanr(gdpColumn, lifeColumn)
print('The correlation is', correlation)
if pValue < 0.05:
    print('It is statistically significant.')
else:
    print('It is not statistically significant.')


# ### Task
# 
# Calculate the correlation between GDP and population.

# **Now go back to the course.**

# ## Exercise 11: Scatterplots
# 
# The dataframe method `plot()` can also produce scatterplots. The `logx` and `logy` arguments  set a logarithmic scale on the corresponding axis.

# In[40]:


get_ipython().run_line_magic('matplotlib', 'inline')
gdpVsLifeClean.plot(x=GDP, y=LIFE, kind='scatter', grid=True, logx=True, figsize = (10, 4))


# ### Tasks
# 
# - Swap the axes of the scatterplot, i.e. show the GDP in the y axis and the life expectancy in the x axis.
# - Display a scatterplot of the GDP and the population.

# **Now go back to the course.**
