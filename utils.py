def from_list_to_candle(data, pair, interval):
    return (
        f"{pair}_{data[0]}_{interval}", # id
        pair, # pair
        data[0], # timestamp
        float(data[2]), # high
        float(data[3]), # low
        float(data[1]), # open
        float(data[4]), # close
        float(data[5]), # volume
        interval # interval
    )