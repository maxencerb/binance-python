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