# import modules for requests and json
from os import closerange
import requests
import json
import time
import hashlib
import hmac
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()

TEST_ENV = os.getenv('TEST_ENV') == '1'

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
    # print(json_data)
    # Filter out the pairs that are SPOT only with limit order possible
    filtered_pairs = [pair for pair in json_data['symbols'] if pair['status'] == 'TRADING' and 'SPOT' in pair['permissions'] and 'LIMIT' in pair['orderTypes']]
    # return the JSON data
    return list(map(lambda x: {
        'symbol': x['symbol'],
        'baseAsset': x['baseAsset'],
        'quoteAsset': x['quoteAsset'],
    }, filtered_pairs))


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

def createOrder(api_key, secret_key, direction, price, amount, pair='BTCUSD_d', orderType='LIMIT'):
    # define the API endpoint
    endpoint = f'v3/order{TEST_ENV and "/test" or ""}'
    # define the API parameters
    params = {
        'symbol': pair,
        'side': direction,
        'type': orderType,
        'timeInForce': 'GTC',
        'quantity': amount,
        'price': price,
        'timestamp': int(time.time()) * 1000
    }
    # make the API call
    response = requests.post(url + endpoint, data={**params, 'signature': get_signature(secret_key, params)}, headers=get_headers(api_key))
    # convert the response to JSON
    json_data = json.loads(response.text)
    # return the JSON data
    return json_data

def get_headers(api_key):
    return {
        'X-MBX-APIKEY': api_key
    }

def get_signature(secret_key: str, params):
    return hmac.new(secret_key.encode(), urlencode(params).encode(), hashlib.sha256).hexdigest()

def get_possible_price_range(pair='BTCUSDC'):
    # define the API endpoint
    endpoint = 'v1/ticker/price'
    # define the API parameters
    params = {'symbol': pair}
    # make the API call
    response = requests.get(url + endpoint, params=params)
    # convert the response to JSON
    json_data = json.loads(response.text)
    # return the JSON data
    return json_data['price']

def cancelOrder(api_key, secret_key, orderId, symbol):
    # define the API endpoint
    endpoint = f'v3/order{TEST_ENV and "/test" or ""}'
    # define the API parameters
    params = {
        'symbol': symbol,
        'orderId': orderId,
        'timestamp': int(time.time()) * 1000
    }
    # make the API call
    response = requests.delete(url + endpoint, data={**params, 'signature': get_signature(secret_key, params)}, headers=get_headers(api_key))
    # convert the response to JSON
    json_data = json.loads(response.text)
    # return the JSON data
    return json_data


if __name__ == '__main__':
    # api_key = os.getenv('BINANCE_API_KEY')
    # secret_key = os.getenv('BINANCE_SECRET_KEY')
    # pair = 'LTCBTC'
    # res = createOrder(api_key, secret_key, 'BUY', get_possible_price_range(pair), '10', pair)
    # print(res)
    getAllSymbols()