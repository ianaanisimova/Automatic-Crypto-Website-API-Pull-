#!/usr/bin/env python
# coding: utf-8

# # Automatic Crypto Website API Pull

# In[2]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'xxxxxx',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[8]:


import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[4]:


df = pd.json_normalize(data['data'])
df['timestamp'] = pd.Timestamp('now')
df


# In[5]:


def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'15',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'de38d0e4-1245-4a8a-b83d-39f0dfb03a0c',
    }
    
    session = Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)       
    df2 = pd.json_normalize(data['data'])
    df2['timestamp'] = pd.Timestamp('now')
    df = pd.concat([df, df2])


# In[6]:


import os 
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API Runner completed successfully')
    sleep(60) #sleep for 1 minute
exit()


# In[9]:


df


# In[17]:


pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[18]:


df


# In[21]:


df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']].mean()
df3


# In[22]:


df4= df3.stack()
df4


# In[23]:


df5 = df4.to_frame(name = 'values')
df5


# In[24]:


df5.count()


# In[27]:


index = pd.Index(range(90))

df6 = df5.reset_index()
df6


# In[33]:


df7 = df6.rename(columns={'level_1': 'percent_change'})
df7


# In[37]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d' ], ['1h', '24h','7d','30d','60d', '90d'])


# In[38]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[39]:


sns.catplot(x='percent_change', y = 'values', hue = 'name', data= df7, kind='point')


# In[42]:


df8 = df[['name', 'quote.USD.price', 'timestamp']]
df8 = df8.query("name == 'Bitcoin'")
df8


# In[43]:


sns.set_theme(style="darkgrid")
sns.lineplot(x='timestamp', y= 'quote.USD.price', data = df8)


# In[ ]:




