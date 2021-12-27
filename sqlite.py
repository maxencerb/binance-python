import sqlite3
from utils import from_list_to_candle

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect('binance.db')

def init_db(conn: sqlite3.Connection):
    c = conn.cursor()

    # Create table for candles
    c.execute('''CREATE TABLE IF NOT EXISTS CANDLES (
                    id TEXT PRIMARY KEY,
                    pair TEXT,
                    timestamp INTEGER,
                    high REAL,
                    low REAL,
                    open REAL,
                    close REAL,
                    volume REAL,
                    interval TEXT
                )''')

    # Create table for last candle of pair
    c.execute('''CREATE TABLE IF NOT EXISTS LAST_CANDLE (
                    pair TEXT PRIMARY KEY,
                    id TEXT
                )''')

    conn.commit()

def __insert_candles(conn: sqlite3.Connection, candles):
    conn = get_connection()
    c = conn.cursor()

    for candle in candles:
        c.execute("INSERT OR IGNORE INTO CANDLES VALUES (?,?,?,?,?,?,?,?,?)", candle)

    conn.commit()

def insert_candles(conn: sqlite3.Connection, candles_list, pair, interval):
    candles = list(map(lambda x: from_list_to_candle(x, pair, interval), candles_list))
    __insert_candles(conn, candles)

def retrieve_candles(conn: sqlite3.Connection, pair, interval):
    c = conn.cursor()
    c.execute("SELECT * FROM CANDLES WHERE pair = ? AND interval = ?", (pair, interval))
    return c.fetchall()