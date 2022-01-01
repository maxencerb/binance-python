# import modules for requests and json
from os import closerange
import requests
import json
import time
import datetime


# define the API URL
url = 'https://api.binance.com/api/'

def getAllSymbols():
    # define the API endpoint
    endpoint = 'v1/exchangeInfo'
    # define the API parameters
    params = {}
    # make the API call
    response = requests.get(url + endpoint, params=params)
    # convert the response to JSON
    json_data = json.loads(response.text)
    # return the JSON data
    return list(map(lambda x: x['symbol'], json_data['symbols']))


def getDepth(direction="asks", pair='BTCUSDC'):
    # define the API endpoint
    endpoint = 'v1/depth'
    # define the API parameters
    params = {'symbol': pair, 'limit': 100}
    # make the API call
    response = requests.get(url + endpoint, params=params)
    # convert the response to JSON
    json_data = json.loads(response.text)
    # return the JSON data
    return json_data[direction]

def getOrderBook(pair='BTCUSDC'):
    # define the API endpoint
    endpoint = 'v1/depth'
    # define the API parameters
    params = {'symbol': pair, 'limit': 100}
    # make the API call
    response = requests.get(url + endpoint, params=params)
    # convert the response to JSON
    json_data = json.loads(response.text)
    # return the JSON data
    return json_data

def get_data_candle(pair='BTCUSDC', interval='1m'):
    # define the API endpoint
    endpoint = 'v1/klines'
    # define the API parameters
    params = {'symbol': pair, 'interval': interval}
    # make the API call
    response = requests.get(url + endpoint, params=params)
    # convert the response to JSON
    json_data = json.loads(response.text)
    # return the JSON data
    return json_data

def createOrder(api_key, secret_key, direction, price, amount, pair='BTCUSD_d', orderType='LimitOrder'):
    # define the API endpoint
    endpoint = '/api/v3/order/test'
    # define the API parameters
    params = {'symbol': pair, 'side': direction, 'type': orderType, 'quantity': amount, 'price': price}
    # make the API call
    response = requests.post(url + endpoint, params=params, headers=get_headers(api_key, secret_key))
    # convert the response to JSON
    # json_data = json.loads(response.text)
    # # return the JSON data
    # return json_data
    return response.text

def get_headers(api_key, secret_key):
    return {
        'X-MBX-APIKEY': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }


import os

api_key = os.getenv('BINANCE_API_KEY')
res = createOrder(api_key, '', 'BUY', '0.000001', '0.000001', 'BTCUSDC')
print(res)