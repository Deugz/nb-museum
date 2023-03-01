#!/usr/bin/env python
# coding: utf-8

# # Exercise notebook 1: Having a go at it
# 
# This Jupyter notebook, for the first part of The Open University's _Learn to Code for Data Analysis_ course, contains code examples and coding activities for you.
# 
# You'll come across steps in the course directing you to this notebook. Once you've done each exercise, go back to the corresponding step and mark it as complete. 

# In[1]:


# this code conceals irrelevant warning messages
import warnings
warnings.simplefilter('ignore', FutureWarning)


# ## Exercise 1: variables and assignments
# 
# A **variable** is a named storage for values. An **assignment** takes a value (like the number 100 below) and stores it in a variable (`deathsInPortugal` below).

# In[2]:


deathsInPortugal = 100


# To display the value stored in a variable, write the name of the variable. 

# In[3]:


deathsInPortugal


# Each variable can store one value at any time, but the value stored can vary over time, by assigning a new value to the variable.

# In[4]:


deathsInPortugal = 100
deathsInPortugal = 140
deathsInPortugal


# Each assignment is written on a separate line. The computer executes the assignments one line at a time, from top to bottom.

# In[5]:


deathsInPortugal = 140
deathsInAngola = 6900
deathsInBrazil = 4400


# ### Task
# 
# Add assignments to the code cell above (or in a new code cell) for the estimated deaths by TB in 2013 in the remaining BRICS countries. The values are as follows: Russia 17000, India 240000, China 41000, South Africa 25000. 
# 
# Don't forget to run the code cell, so that the new variables are available for the exercises further below.
# 
# **Now go back to the course.**

# ## Exercise 2: expressions
# 
# An **expression** is a fragment of code that has a value. A variable name, by itself, is an expression: the expression's value is the value stored in the variable. In Jupyter notebooks, if the last line of a code cell is an expression, then the computer will show its value when executing the cell. 

# In[6]:


deathsInPortugal


# By contrast, a **statement** is a command for the computer to do something. Commands don't produce values, and therefore the computer doesn't display anything.

# In[7]:


deathsInPortugal = 140


# More complex expressions can be written using the arithmetic **operators** of addition (`+`), substraction (`-`), multiplication (`*`) and division (`/`). For example, the total number of deaths in the three countries is:

# In[8]:


deathsInAngola + deathsInBrazil + deathsInPortugal


# If the calculated value needs to be used later on in the code, it has to be stored in a variable. In general, the right-hand side of an assignment is an expression; its value is calculated (the expression is **evaluated**) and stored in the variable.

# In[9]:


totalDeaths = deathsInAngola + deathsInBrazil + deathsInPortugal
totalDeaths


# The average number of deaths is the total divided by the number of countries.

# In[10]:


totalDeaths / 3


# The average could also be calculated with a single expression.

# In[11]:


(deathsInAngola + deathsInBrazil + deathsInPortugal) / 3


# The parentheses (round brackets) are necessary to state that the sum has to be calculated before the division. Without parentheses, Python follows the conventional order used in mathematics: divisions and multiplications are done before additions and subtractions.

# In[12]:


deathsInAngola + deathsInBrazil + deathsInPortugal / 3


# ### Task
# 
# - In the cell below, write code to calculate the total number of deaths in the five BRICS countries (Brazil, Russia, India, China, South Africa) in 2013. Run the code to see the result, which should be 327400.

# In[ ]:





# - In the cell below, write code to calculate the average number of deaths in the BRICS countries in 2013. Run the code to see the result, which should be 65480.

# In[ ]:





# **Now go back to the course.**

# ## Exercise 3: functions quiz 
# 
# A **function** takes zero or more values (the function's **arguments**) and **returns** (produces) a value. To **call** (use) a function, write the function name, followed by its arguments within parentheses (round brackets). Multiple arguments are separated by commas. Function names follow the same rules and conventions as variable names. A function call is an expression: the expression's value is the value returned by the function.
# 
# Python provides two functions to compute the **maximum** (largest) and **minimum** (smallest) of two or more values.

# In[13]:


max(deathsInBrazil, deathsInPortugal)


# In[14]:


min(deathsInAngola, deathsInBrazil, deathsInPortugal)


# The **range** of a set of values is the difference between the maximum and the minimum.

# In[15]:


largest = max(deathsInBrazil, deathsInPortugal)
smallest = min(deathsInBrazil, deathsInPortugal)
deathsRange = largest - smallest
deathsRange


# ### Tasks
# 
# Answer the quiz questions in the course. All of them can be answered by editing the above code cell. Don't forget that you can use TAB-completion to quickly write the variable names of the remaining BRICS countries, namely Russia, India, China and South Africa (Brazil is already in the code above).

# ## Exercise 4: comments
# 
# **Comments** start with the hash sign (`#`) and go until the end of the line. They're used to annotate the code, e.g. to indicate the units of values.

# In[16]:


# population unit: thousands of inhabitants
populationOfPortugal = 10608

# deaths unit: inhabitants
deathsInPortugal = 140

# deaths per 100 thousand inhabitants
deathsInPortugal * 100 / populationOfPortugal


# ### Task
# 
# Calculate the deaths per 100 thousand inhabitants for Brazil. Its population in 2013 was roughly 200 million and 362 thousand people. You should obtain a result of around 2.2 deaths per 100 thousand people.

# **Now go back to the course.**

# ## Exercise 5: pandas quiz
# 
# All programs in this course must start with the following **import statement**, to load all the code from the pandas **module**.

# In[17]:


from pandas import *


# The words in boldface (`from` and `import`) are **reserved words** of the Python language; they cannot be used as names.
# 
# ### Task
# 
# Answer the quiz questions in the course. You can change the above line of code to find out the answers.

# ## Exercise 6: selecting a column
# 
# The `read_excel()` function takes a **string** with the name of an Excel file, and returns a **dataframe**, the pandas representation of a table. The computer reports a **file not found** error if the file is not in the same folder as this notebook, or the file name is misspelt.

# In[18]:


data = read_excel('WHO POP TB some.xls')
data


# The expression `dataFrame[columnName]` evaluates to the column with the given name (a string). Column names are case sensitive. Misspelling the column name will result in a rather long **key error** message. You can see what happens by changing the string in the next code cell (e.g. replace `TB` by `tb`) and running it. Don't forget to undo your change and run the code again.

# In[19]:


tbColumn = data['TB deaths']
tbColumn


# ### Task
# 
# In the next cell, select the population column and store it in a variable (you'll use it in the next exercise). You need to scroll back to the start of the exercise to see the column's name.

# In[ ]:





# **Now go back to the course.**

# ## Exercise 7: calculations on a column
# 
# 
# A **method** is a function that can only be called in a certain context, like a dataframe or a column. A **method call** is of the form `context.methodName(argument1, argument2, ...)`.   
# 
# Pandas provides several column methods, including to calculate the sum, the largest, and the smallest of the numbers in a column, as follows.

# In[20]:


tbColumn.sum()


# In[21]:


tbColumn.max()


# In[22]:


tbColumn.min()


# The **mean** of a collection of numbers is the sum of those numbers divided by how many there are.

# In[23]:


tbColumn.sum() / 12


# In[24]:


tbColumn.mean()


# The **median** of a collection of numbers is the number in the middle, i.e. half of the numbers are below the median and half  are above.

# In[25]:


tbColumn.median()


# ### Tasks
# 
# Use the population column variable from the previous exercise to calculate:
# 
# - the total population

# In[ ]:





# - the maximum population

# In[ ]:





# - the minimum population

# In[ ]:





# **Now go back to the course.**

# ## Exercise 8: sorting on a column
# 
# The dataframe method `sort_values()` takes as argument a column name and returns a new dataframe, with rows in ascending order according to the values in that column.

# In[26]:


data.sort_values('TB deaths')


# Sorting doesn't change the original table.

# In[27]:


data # rows still in original order


# Sorting on a column that has text will put the rows in alphabetical order.

# In[28]:


data.sort_values('Country')


# ### Task
# 
# Sort the same table by population, to quickly see which are the least and the most populous countries.

# **Now go back to the course.**

# ## Final quiz: Calculations over columns
# 
# This information will help you to answer questions in the final quiz.
# 
# The value of an arithmetic expression involving columns is a column. In evaluating the expression, the computer computes the expression for each row.

# In[29]:


deathsColumn = data['TB deaths']
populationColumn = data['Population (1000s)']
rateColumn = deathsColumn * 100 / populationColumn
rateColumn


# To add a new column to a dataframe, 'select' a non-existing column, i.e. with a new name, and assign to it.

# In[30]:


data['TB deaths (per 100000)'] = rateColumn
data


# ### Tasks
# 
# Add code to calculate:
# 
# - the range of the population, in thousands of inhabitants

# In[ ]:





# - the mean of the death rate

# In[ ]:





# - the median of the death rate

# In[ ]:





# Now you can answer the questions in the **final quiz**.
