#!/usr/bin/env python
# coding: utf-8

# In[59]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd

df = pd.read_excel('../input/sales_data.xlsx')


# In[ ]:


df[140:145]


# In[ ]:


patternDel = '^C[0-9][0-9][0-9][0-9][0-9][0-9]'
indextoDelete = df[df['transaction id'].str.contains(patternDel)==True].index
# Delete these row indexes from dataFrame
df.drop(indextoDelete,inplace=True)
df.reset_index(inplace=True)


# In[ ]:


df = df.drop(['index'],axis=1)
df[140:145]


# **Number of unique products**

# In[ ]:


unique_products = pd.value_counts(df['product id'])
number_of_unique_products = pd.Series({'nunique': len(unique_products), 'unique values': unique_products.index.tolist()})
unique_products.append(number_of_unique_products)


# **Number of unique transactions**

# In[ ]:


unique_transactions = pd.value_counts(df['transaction id'])
number_of_unique_transacations = pd.Series({'nunique': len(unique_transactions), 'unique values': unique_transactions.index.tolist()})
unique_transactions.append(number_of_unique_transacations)


# **Adding new columns for each product depending on the number of units in transaction**
# <br><br>
# &nbsp; &nbsp; &nbsp; - Column is named product_price
# <br>
# &nbsp; &nbsp; &nbsp; - Column is calculated as 'unit price' * 'quantity sold'

# In[ ]:


df['product_price'] = df['unit price'] * df['quantity sold']
original_df = df


# In[ ]:


df.head()


# ### Checking the minimum and maximum date in the sales data
# We find that we have typically one year of sales data.
# <br> Minimum Timestamp - **1st December 2010**
# <br> Maximum Timestamp - **9th December 2010**

# In[ ]:


df['transaction timestamp'].min(),df['transaction timestamp'].max()


# In[ ]:


grouped_df = df.groupby(['transaction timestamp'])['product_price'].sum().reset_index()
grouped_df=grouped_df.set_index('transaction timestamp')


# ### **Level Analysis**
#  - **Weekly** Level 
#  - **Semi-Montly** Level
#  - **Monthly** Level
# ***
# ### Metrics used for time series analysis
# 1. **Sum** of product_prices of all transactions
# 2. **Mean** of product prices of all transactions

# In[ ]:


weekly_resampled_data_sum = grouped_df['product_price'].resample('W').sum()
weekly_resampled_data_mean = grouped_df['product_price'].resample('W').mean()


# In[ ]:


import matplotlib.pyplot as plt
weekly_resampled_data_sum.plot(figsize=(15, 6))
plt.show()


# In[ ]:


weekly_resampled_data_mean = weekly_resampled_data_mean.interpolate(axis=0)
weekly_resampled_data_mean.plot(figsize=(15, 6))
plt.show()


# In[ ]:


semimonthly_resampled_data_sum = grouped_df['product_price'].resample('MS').sum()
semimonthly_resampled_data_mean = grouped_df['product_price'].resample('MS').mean()


# In[ ]:


semimonthly_resampled_data_sum.plot(figsize=(15, 6))
plt.show()


# In[ ]:


semimonthly_resampled_data_mean.plot(figsize=(15, 6))
plt.show()


# In[ ]:


monthly_resampled_data_sum = grouped_df['product_price'].resample('M').sum()
monthly_resampled_data_mean = grouped_df['product_price'].resample('M').mean()


# In[ ]:


monthly_resampled_data_sum.plot(figsize=(15, 6))
plt.show()


# In[ ]:


monthly_resampled_data_mean.plot(figsize=(15, 6))
plt.show()


# In[ ]:


df = original_df


# ### Extracting the transaction country
# 
# **Based on the transaction country (for countries where number of transactions is greater than )**

# In[ ]:


list_of_countries = pd.value_counts(df['transaction country'])

