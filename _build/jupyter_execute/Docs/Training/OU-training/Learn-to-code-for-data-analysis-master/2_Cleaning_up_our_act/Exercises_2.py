#!/usr/bin/env python
# coding: utf-8

# # Exercise notebook 2: Cleaning up our act
# This Jupyter notebook, for the second part of The Open University's _Learn to code for Data Analysis_ course, has code examples and coding activities for you. Remember to run the code in this notebook before you start.
# 
# You'll come across steps in the course directing you to this notebook. Once you've done each exercise, go back to the corresponding step and mark it as complete. 

# In[1]:


import warnings
warnings.simplefilter('ignore', FutureWarning)

from pandas import *


# ## Exercise 1: Dataframes and CSV files
# 
# To read a CSV file into a dataframe you need to call the pandas function called <code>read_csv()</code>. The simplest usage of this function is with a single argument, a string that holds the name of the CSV file, for example.

# In[2]:


df = read_csv('WHO POP TB all.csv')


# ### Dataframe attributes
# 
# A dataframe attribute is like a variable that can only be accessed in the context of a dataframe. One such attribute is <code>columns</code> which holds a dataframe's column names.

# In[3]:


df.columns


# ### Dataframe rows
# A dataframe has a default integer index for its rows, which starts at zero. The `iloc` attribute can be used to obtain the row at the given index.

# In[4]:


df.iloc[0] # first row, index 0


# In[5]:


df.iloc[2] # third row, index 2


# ### The <code>head()</code> method
# 
# The `head()` method returns a dataframe with the first rows, as many as given in the argument. By default, if the argument is missing, it returns the first five rows.

# In[6]:


df.head() # first five rows


# In[7]:


df.head(7) # first seven rows


# ### The <code>tail()</code> method
# The <code>tail()</code> method is similar to the <code>head()</code> method. If no argument is used, the last five rows of the dataframe are returned, otherwise the number of rows returned is dependent on the argument.

# In[8]:


df.tail() # last five rows


# ### Selecting and displaying columns in a dataframe
# You found in Week 1 that you can select and display the values for a single dataframe column by puting the name of the column (in quotes) within square brackets immediately after the dataframe's name. However you can also select and display the values for multiple columns too.
# 
# To get multiple columns you need to use a list. A list in Python is a number of items separated by commas within square brackets, for example `['Country', 'Population (1000s)']`. This list is then put within square brackets immediately after the dataframe's name. The resulting expression represents a new dataframe, just with those columns, and therefore any dataframe method can be applied to it, like for example `head()`:

# In[9]:


df[['Country', 'Population (1000s)']].head()


# ### Applying methods to a dataframe column
# The `iloc` attribute and the <code>head()</code> and <code>tail()</code> methods discussed above can be used with single columns.

# In[10]:


df['TB deaths'].iloc[2] # third value of deaths column


# In[11]:


df['Population (1000s)'].tail() # last five values of population column      


# ### Tasks
# 
# In the code cell below, write the code to get and display the 55th row in the dataframe <code>df</code>.

# In[ ]:





# In the code cell below write the code to display the first 10 rows of the dataframe <code>df</code>.

# In[ ]:





# In the code cell below, select and display the first eight rows from the <code>'Country'</code> and <code>'TB deaths'</code> columns.

# In[ ]:





# **Now go back to the course.**

# ## Exercise 2: Comparison operators
# Python has the following comparison operators:
# 
#     == (equals)
#     != (not equal)
#     < (less than)
#     > (greater than)
#     <= (less than or equal to)
#     >= (greater than or equal to)
# 
# The following code will get and display all the rows in `df` where it is `True` that the value in the `'Population (1000s)'` column is greater than `80000`.

# In[12]:


df[df['Population (1000s)'] > 80000]         


# ### Task
# In the code cell below write code to find all the rows in <code>df</code> where TB deaths exceed 10000.

# In[ ]:





# **Now go back to the course.**

# ## Exercise 3: Bitwise operators
# 
# Pandas has two operators to make more complicated queries. Use the operator `&` (means 'and') to select rows where two conditions are both true. Use the operator `|` (means 'or') to select rows where at least one condition is true. Don't forget to put parentheses around _each_ comparison. For example, the following expression selects only countries with a population over 80 million inhabitants **and** with more that 10 thousand deaths.

# In[13]:


df[(df['Population (1000s)'] > 80000) & (df['TB deaths'] > 10000)]


# If the same columns will be used repeatedly in the program, the code becomes more readable if written as follows:

# In[14]:


population = df['Population (1000s)']
deaths = df['TB deaths']
df[(population > 80000) & (deaths > 10000)]  


# ### Task
# In the code cell below find  all the countries where the Population (1000s) is **less than or equal to** 50000 **or** TB deaths are **greater than or equal to** 20000.

# In[ ]:





# **Now go back to the course.**

# ## Exercise 4: Display rows from dataframe
# 
# You have downloaded the file London_2014.csv from our website, it can now be read into a dataframe.

# In[15]:


london = read_csv('London_2014.csv')
london.head()


# ### Removing initial spaces
# 
# There are too many columns for the dataframe to fit horizontally in this notebook, but they can be displayed separately.

# In[16]:


london.columns


# This shows that <code>' Max Wind SpeedKm/h'</code> is prefixed by a space, as are other columm names such as <code>' Mean Humidity'</code> and <code>' Max Sea Level PressurehPa'</code>.
# 
# The  <code>read_csv()</code> function has interpreted spaces after commas as being part of the next value. This can be rectified  easily by adding another argument to the <code>read_csv()</code> function to skip the initial spaces after a comma.

# In[17]:


london = read_csv('London_2014.csv', skipinitialspace=True)


# ### Removing extra characters
# 
# Another problem shown above is that the final column is called <code>'WindDirDegrees&lt; br /&gt;'</code>.
# 
# When the dataset was exported from the Weather Underground web site, HTML line breaks were automatically added to each line in the file which <code>read_csv()</code> has interpreted as part of the column name and its values. This can be seen more clearly by looking at more values in the final column:

# In[18]:


london['WindDirDegrees<br />'].head()


# <code>'WindDirDegrees&lt; br /&gt;'</code> can be changed to <code>'WindDirDegrees'</code> with the <code>rename()</code> method as follows:

# In[19]:


london = london.rename(columns={'WindDirDegrees<br />' : 'WindDirDegrees'})


# To remove the <code>'&lt; br /&gt;'</code> html line breaks from the values in the <code>'WindDirDegrees'</code> column you need to use the string method <code>rstrip()</code> which is used to remove characters from the *end* or 'rear' of a string:

# In[20]:


london['WindDirDegrees'] = london['WindDirDegrees'].str.rstrip('<br />')


# Display the first few rows of the <code>'WindDirDegrees'</code> to confirm the change:

# In[21]:


london['WindDirDegrees'].head()


# ### Missing values
# 
# Missing (also called null or not available) values are marked as NaN (not a number) in dataframes.

# In[22]:


london['Events'].tail()


# The `isnull()` method returns `True` for each row in a column that has a null value. The method can be used to select and display those rows. Scroll the table below to the right to check that the events column is only showing missing values.

# In[23]:


london[london['Events'].isnull()]


# One way to deal with missing values is to replace them by some value. The column method `fillna()` fills all not available value cells with the value given as argument. In the example below, each missing event is replaced by the empty string.

# In[24]:


london['Events'] = london['Events'].fillna('')
london[london['Events'].isnull()]


# The empty dataframe (no rows) confirms there are no more missing event values.
# 
# Another way to deal with missing values is to ignore rows with them. The `dropna()` dataframe method returns a new dataframe where all rows with at least one non-available value have been removed.

# In[25]:


london.dropna()


# Note that the table above has fewer than 251 of the original 365 rows, so there must be further null values besides the 114 missing events.

# ### Changing the value type of a column

# The type of every column in a dataframe can be determined by looking at the dataframe's `dtypes` attribute, like this:

# In[26]:


london.dtypes


# The type of all the values in a column can be changed using the <code>astype()</code> method. The following code will change the values in the <code>'WindDirDegrees'</code> column from strings (`object`) to integers (<code>int64</code>).

# In[27]:


london['WindDirDegrees'] = london['WindDirDegrees'].astype('int64')   


# The function `to_datetime()` is needed to change the values in the `'GMT'` column from strings (`object`) to dates (`datetime64`):

# In[28]:


london['GMT'] = to_datetime(london['GMT'])
london.dtypes


# Values of type `datetime64` can be created using the `datetime()` function, provided by the package of the same name. The first integer argument is the year, the second the month and the third the day. 
# The code below will get and display the row in the dataframe whose `'GMT'` value is 4th June 2014.

# In[29]:


from datetime import datetime

london[london['GMT'] == datetime(2014, 6, 4)] 


# Queries such as 'Return all the rows where the date is between 8 December and 12 December' can be made:

# In[30]:


dates = london['GMT']
start = datetime(2014, 12, 8)
end = datetime(2014, 12, 12)
london[(dates >= start) & (dates <= end)]


# ### Tasks
# 
# Now that the wind direction is given by a number, write code to select all days that had a northerly wind. Hint: select the rows where the direction is greater than or equal to 350 **or** smaller than or equal to 10, as the compass rose shows.

# In[ ]:





# In the code cell below, write code to get and display all the rows in the dataframe that are beween 1 April 2014 and 
# 11 April 2014.

# In[ ]:





# In the cell below, write two lines of code to display the first five rows that have a missing value in the `'Max Gust SpeedKm/h'` column. Hint: first select the missing value rows and store them in a new dataframe, then display the first five rows of the new dataframe.

# In[ ]:





# **Now go back to the course.**

# ## Exercise 5: Every picture tells a story
# 
# The following line of code tells Jupyter to display inside this notebook any graph that is created.

# In[31]:


get_ipython().run_line_magic('matplotlib', 'inline')


# The `plot()` method can make a graph of the values in a column. Gridlines are turned on by the `grid` argument.

# In[32]:


london['Max Wind SpeedKm/h'].plot(grid=True)


# The graph can be made bigger by giving the method a `figsize=(x,y)` argument where `x` and `y` are integers that determine the length of the x-axis and y-axis.

# In[33]:


london['Max Wind SpeedKm/h'].plot(grid=True, figsize=(10,5))


# Multiple lines can be plotted by selecting multiple columns.

# In[34]:


london[['Max Wind SpeedKm/h', 'Mean Wind SpeedKm/h']].plot(grid=True, figsize=(10,5))


# ### Task
# 
# In the cell below, write code to plot the minimum, mean, and maximum temperature during 2014 in London.

# In[ ]:





# **Now go back to the course.**

# ## Exercise 6: Changing a dataframe's index
# Changing the dataframe's index from the default to `datetime64` values is done by assigning to the dataframe's `index` attribute the contents of the `'GMT`' column, like this:

# In[35]:


london.index = london['GMT']
london.head(2)


# The `iloc` attribute can still be used to get and display rows by number, but now you can now also use the `datetime64` index to get a row by date, using the dataframe's `loc` attribute, like this:

# In[36]:


london.loc[datetime(2014, 1, 1)]


# A query such as *'Return all the rows where the date is between December 8th and December 12th'* can now be done  succinctly like this:

# In[37]:


london.loc[datetime(2014,12,8) : datetime(2014,12,12)]

#The meaning of the above code is get the rows beween and including 
#the indices datetime(2014,12,8) and datetime(2014,12,12)


# Now we have a `datetime64` index, let's plot `'Max Wind SpeedKm/h'` again:

# In[38]:


london['Max Wind SpeedKm/h'].plot(grid=True, figsize=(10,5))


# Now it is much clearer that the worst winds were in mid February.
# 
# ### Task
# Use the code cell below to plot the values of `'Mean Humidity'` during spring (full months of March, April and May).

# In[ ]:





# **Now go back to the course.**
