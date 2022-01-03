# Binance API from scratch in Python

The goal of this project is to learn how to use the Binance API from scratch in Python.

For that, I used the docs from binance api team.

The project is divided into three parts:

1. Calls to the Binance API and data cleaning (transformations on data)
2. Saving the data in a database (SQLite)
3. Creating an arbitrage bot

## Usage for this repo

In order to use this repo, you need to install the packages as follows:

```bash
pip install -r requirements.txt
```

Then create a .env file with the following variables:

```env
BINANCE_API_KEY=<your_api_key>
BINANCE_SECRET_KEY=<your_secret_key>
TEST_ENV=1
```

The test env variable is used for the `createOrder` function. If it is set to 1, the function will create an order on the test environment, otherwise it will create an order on the main environment.

You can also export those variables in your shell environment.

## Calls to the Binance API

### Retrieve Data

In order to retrieve data from the Binance API, I used the requests library uniquely. Retrieving data is free and does not require an API key.

Retrievable data can either be exchange informations, market data, or historical data in the form of candlesticks.

### Post Data

Posting data here consists of placing an order. It's hidden in the docs but there are a few steps in order to retrieve data. First you need to create an API key. You will be given a secret key too.

In order to place an order, you need to create a signed payload. The payload contains a timestamp plus the transaction data in order for the transaction to be valid for a certain time frame.

The signature is a hmac sha256 hash of the payload with the secret key as the key. The API key is only used in the header of the request.

```py
params = {
    'symbol': pair,
    'side': direction,
    'type': orderType,
    'timeInForce': 'GTC',
    'quantity': amount,
    'price': price,
    'timestamp': int(time.time()) * 1000
}

# Get the signature from the payload
# form of the payload : 'param=value&param=value&...'
# This fomat for the payload can be obtained with `urlencode` function from the `urllib` library
signature = hmac.new(secret_key.encode(), urlencode(params).encode(), hashlib.sha256).hexdigest()

requests.post(url + endpoint, data={**params, 'signature': signature}, headers=get_headers(api_key))
```

The headers are retrieved from the get_headers function which is very simple :

```py
def get_headers(api_key):
    return {
        'X-MBX-APIKEY': api_key
    }
```

## Store Data

The data is stored in a SQLite database. The schema is simple and can be found in the `sqlite.py` file.

Data can be retrieved from the database using the `retrieve_candles` function.

## Arbitrage bot

The first step is to retrieve all SPOT markets that accept LIMIT orders from the Binance API. The next thing is to search trhough all possible market trio (BTC/USDT, ETH/USDT, ETH/BTC for example) and find the best arbitrage opportunity. A limit is set to the number of trio. It is not optimized as it takes the first market trio it finds. Nontheless, it works.

Then the goal is to use the price of these markets based on order books to calculate the potential profits. No order will be placed in this file. So the TEST_ENV variable must be set to 1.