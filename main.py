from binance import get_data_candle
from sqlite import insert_candles, init_db, get_connection, retrieve_candles

from dotenv import load_dotenv

def main():
    candles_list = get_data_candle('BTCUSDC', '1m')
    conn = get_connection()
    init_db(conn)
    insert_candles(conn, candles_list, 'BTCUSDC', '1m')

    retrieved = retrieve_candles(conn, 'BTCUSDC', '1m')
    print(retrieved)
    conn.close()