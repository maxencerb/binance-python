from binance import get_data_candle, getOrderBook, getAllSymbols, getDepth, createOrder, cancelOrder
from sqlite import insert_candles, init_db, get_connection, retrieve_candles

def FindAllArbitrageMarkets(limit=10):
    markets = getAllSymbols()
    arbitrage_markets = []
    possible_market = []

    def add_possible_market(i, j, possible_market):
        possible_market_list = list(possible_market)
        if len(possible_market_list) > 0:
            arbitrage_markets.append({
                'market1': markets[i],
                'market2': markets[j],
                'possible_market': possible_market_list[0]
            })

    for i in range(len(markets)):
        for j in range(i+1, len(markets)):
            if len(arbitrage_markets) >= limit:
                break
            # Continue if at least one of the crypto is both in market 1 and market 2
            if markets[i]['baseAsset'] == markets[j]['baseAsset']:
                possible_market = filter(lambda x: (x['quoteAsset'] == markets[i]['quoteAsset'] and x['baseAsset'] == markets[j]['quoteAsset']) or (x['quoteAsset'] == markets[j]['quoteAsset'] and x['baseAsset'] == markets[i]['quoteAsset']), markets)
                add_possible_market(i, j, possible_market)
            elif markets[i]['quoteAsset'] == markets[j]['baseAsset']:
                possible_market = filter(lambda x: (x['quoteAsset'] == markets[i]['baseAsset'] and x['baseAsset'] == markets[j]['quoteAsset']) or (x['quoteAsset'] == markets[j]['quoteAsset'] and x['baseAsset'] == markets[i]['baseAsset']), markets)
                add_possible_market(i, j, possible_market)
            elif markets[i]['quoteAsset'] == markets[j]['quoteAsset']:
                possible_market = filter(lambda x: (x['quoteAsset'] == markets[i]['baseAsset'] and x['baseAsset'] == markets[j]['baseAsset']) or (x['quoteAsset'] == markets[j]['baseAsset'] and x['baseAsset'] == markets[i]['baseAsset']), markets)
                add_possible_market(i, j, possible_market)
    return arbitrage_markets

def getMarketPrice(market):
    depth = getDepth()
    return depth[0]['price']

print(getMarketPrice('LTCBTC'))