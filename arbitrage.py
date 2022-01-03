from binance import get_data_candle, getOrderBook, getAllSymbols, getDepth, createOrder, cancelOrder
from sqlite import insert_candles, init_db, get_connection, retrieve_candles

def FindAllArbitrageMarkets(limit=10):
    markets = getAllSymbols()
    arbitrage_markets = []
    possible_market = []

    def add_possible_market(i, j, possible_market):
        possible_market_list = list(possible_market)
        if len(possible_market_list) > 0:
            arbitrage_markets.append([
                possible_market_list[0],
                markets[i],
                markets[j]
            ])

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

def getPrice(pair, direction='asks'):
    depth = getDepth(direction, pair)
    return float(depth[0][0])

def getArbitragePrice(arbitrage_markets):
    arbitrage_price = []
    for i in range(len(arbitrage_markets)):
        direction = 'asks'
        if i > 0 and (arbitrage_markets[i]['quoteAsset'] == arbitrage_markets[i-1]['quoteAsset'] or arbitrage_markets[i]['quoteAsset'] == arbitrage_markets[i-1]['baseAsset']):
            direction = 'bids'
        arbitrage_price.append(getPrice(arbitrage_markets[i]['symbol'], direction=direction))
        if direction == 'bids':
            arbitrage_price[i] = 1/arbitrage_price[i]
    return arbitrage_price

def fromArbitragePriceToPercentage(arbitrage_price):
    price = 1
    for prices in arbitrage_price:
        price *= prices
    return price - 1

def formatProfit(profit):
    return f'{profit * 100}%'

def main():
    arbitrage_markets = FindAllArbitrageMarkets(limit=10)
    arbitrage_prices = [getArbitragePrice(arbitrage_market) for arbitrage_market in arbitrage_markets]
    profits = [fromArbitragePriceToPercentage(arbitrage_price) for arbitrage_price in arbitrage_prices]
    for i in range(len(arbitrage_markets)):
        print(f'{arbitrage_markets[i][0]} -> {arbitrage_markets[i][1]} -> {arbitrage_markets[i][2]}')
        print(f'Profit : {formatProfit(profits[i])}')
        print('\n=========================================================\n')

if __name__ == '__main__':
    main()