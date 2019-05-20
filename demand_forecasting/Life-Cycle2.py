#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# import raw data
def import_data(url):
    df = pd.read_csv(url)
    return df


# In[4]:


# import data
gridwatch_df = import_data("gridwatch.csv")

# change the labels
gridwatch_df = gridwatch_df.rename(columns={' timestamp':'ds', ' demand':'y'})
gridwatch_df.head()


# In[5]:


gridwatch_df.y = gridwatch_df.y.astype(int)


# In[6]:


# turn strings into datetime
gridwatch_df['ds'] = pd.to_datetime(gridwatch_df.iloc[:,0], format='%Y-%m-%d %H:%M:%S')


# In[7]:


length = len(gridwatch_df)
length # hold test size of 60
train_size = length-60


# In[7]:


# Creating train and test set, do just 10% of the data
# Index 10392 marks the end of October 2013 
train_df = gridwatch_df[: train_size] 
test_df = gridwatch_df[train_size :]


# In[8]:


# plotting the actual data
plt.figure(figsize=(15,8))
plt.plot(train_df['ds'], train_df['y'])
plt.plot(test_df['ds'], test_df['y'])
plt.title('forecasting')
plt.show()


# In[9]:


# try fbprophet
import fbprophet
from fbprophet import Prophet


# In[10]:


# create instance of prophet
two_years_data = length - (6*24*30*24)
df2 = gridwatch_df[two_years_data:]
df2.reset_index(inplace=True)
df2.tail()


# In[11]:


# fit the data (only 1/7th of it)
# from lloking at data, we can set high cap to 55,000 and low to 15,000
# this gives us a workable range
df2['cap'] = 55000
df2['floor'] = 15000

df2_prophet = Prophet( changepoint_prior_scale=0.10, growth='logistic')
df2_prophet.add_country_holidays(country_name='UK')
df2_prophet.fit(df2)


# In[12]:


# future predicted values dataset, provides hourly predictions ahead of time
# periods will be a variable
future = df2_prophet.make_future_dataframe(periods=24, freq='H')
future['cap'] = 55000
future['floor'] = 15000
future.tail()


# In[13]:


# forecast uncertainty for future predicted points
forecast = df2_prophet.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head()


# In[14]:


# plot, black dots are actual points. blue ine is prediction
df2_prophet.plot(forecast, xlabel='date', ylabel='consumption (kWH)')


# In[15]:


df2_prophet.plot_components(forecast)


# In[16]:


# now for evaluating our model
from fbprophet.diagnostics import cross_validation


# In[17]:


def mean_absolute_percentage_error(y_true, y_pred):
    '''Take in True and Predicted and calculate the mean av percentage score'''
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true-y_pred)/y_true))*100


# In[1]:


# calculating Mininmum absolute percentage error (MAPE)
# mape_baseline = mean_absolute_percentage_error(cv_results.y, cv_results.yhat)


# In[ ]:


# predicting in hourly periods because of hourly data
# cv_results = cross_validation(df2_prophet, initial='1500 hours', period='23 hours', horizon='400 hours')


# In[ ]:


## To get the right future data, look at the forecast and predict
# output over next 24 hour period with uncertainties

