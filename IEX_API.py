#!/usr/bin/env python
# coding: utf-8

import os
import requests

base_url = 'https://cloud.iexapis.com/v1'
sandbox_url = 'https://sandbox.iexapis.com/stable'

token = os.environ.get('IEX_TOKEN')
params = {'token': token}

resp = requests.get(base_url + '/status')
print(resp)
print(resp.json())

# Historical prices endpoint
resp = requests.get(base_url+'/stock/AAPL/chart', params=params)
resp.raise_for_status()
print(resp.json())

# Converting response to a Pandas DataFrame
import pandas as pd
df = pd.DataFrame(resp.json())
print(df.head())

# Create a function to access historical data
def historical_data(_symbol, _range=None, _date=None):
    endpoint = f'{base_url}/stock/{_symbol}/chart'
    if _range:
        endpoint += f'/{_range}'
    elif _date:
        endpoint += f'/date/{_date}'
    
    resp = requests.get(endpoint, params=params)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


appl_3m_df = historical_data('AAPL', _range='3m')
print(appl_3m_df.head())

appl_april_20_df = historical_data('AAPL', _date=20200420)
print(appl_april_20_df.head())

# Using the sandbox environment 
''' This requires a new sandbox token. You can save it as an environment variable (recommended)
or hard code it. You will also need to activate the sanbox environment from within the IEX console.'''

sandbox_params = {'token': 'your_sandbox_api_token'} 
resp = requests.get(sandbox_url+'/stock/AAPL/chart', params=sandbox_params)
resp.raise_for_status()
print(resp.json())

# Earnings Today
endpoint = '/stock/market/today-earnings'
resp = requests.get(base_url+endpoint, params=params)
resp.raise_for_status()
print(resp.json())

# News
endpoint = '/stock/TSLA/news'
resp = requests.get(base_url+endpoint, params=params)
resp.raise_for_status()
print(resp.json())

# Investor Exchange Data
payload = params.copy()
payload['symbols'] = 'TSLA, NFLX'
resp = requests.get(base_url+'/tops/last', params=payload)
resp.raise_for_status()
print(resp.json())