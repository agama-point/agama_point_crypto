import time, datetime
import sqlite3

__version__ = "0.1.0"

DEBUG = True
DB_NAME = "data_db/blockchain.db"


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


def init_tables():
    try:
        print("DB_NAME",DB_NAME)
        if DEBUG: print("[create table blocks]")
        conn.execute('''CREATE TABLE blocks
                (bid INTEGER PRIMARY KEY,
                hid TEXT,
                timestamp INTEGER,
                tx_count INTEGER,
                note TEXT)''') # hid (hash id), imestamp (UNIX time)
        
        if DEBUG: print("[create table txs]")
        conn.execute('''CREATE TABLE txs
                (tid INTEGER PRIMARY KEY,
                bid INTEGER,
                txid TEXT,
                note TEXT)''')
        
        if DEBUG: print("[create table adrval]") # io - counbase, input, output
        conn.execute('''CREATE TABLE adrval
                (id INTEGER PRIMARY KEY,
                bid INTEGER,
                tid INTEGER,
                io TEXT,
                adr TEXT,
                type TEXT,
                val TEXT,
                nbid INTEGER)''') # val INTEGER Err?

    except:
        print("Err. DB exist?")


"""
sql = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
data = ("John Doe", 25, "johndoe@example.com")
cursor.execute(sql, data)
"""


def add_block(bid, hid, timestamp, tx_count):
    if DEBUG: print("> DEBUG LIB add_block", bid, hid, timestamp, tx_count)
    try:
        conn.execute(f"INSERT INTO blocks (bid, hid, timestamp, tx_count, note) VALUES ('{bid}', '{hid}','{timestamp}','{tx_count}','')")
        conn.commit()
    except:
        print("Err. unique index exist")


def add_tx(bid, txid):
    if DEBUG: print("> DEBUG LIB add_tx", bid,txid)
    try:
        conn.execute(f"INSERT INTO txs (bid, txid) VALUES ('{bid}', '{txid}')")
        conn.commit()
    except:
        print("Err. add_tx")


def add_adrval(bid, tid, io, adr, type, val, nbid): # next bid from get_addr
    if DEBUG: print("> DEBUG LIB add_adrval", bid, tid, io, adr, type, val, nbid)
    try:
        conn.execute(f"INSERT INTO adrval (bid, tid, io, adr, type, val, nbid) VALUES ('{bid}','{tid}', '{io}','{adr}','{type}','{val}','{nbid}')")
        conn.commit()
    except:
        print("Err. add_adrval")


def get_tx_uid(tx):
    cursor = conn.execute(f"SELECT * from txs WHERE txid='{tx}'")
    ret = None
    for row in cursor:
        if DEBUG: print("> DEBUG LIB for [get_tx_uid]",row[0])
        ret = row[0]

    return ret # first item


def get_addr(addr):
    cursor = conn.execute(f"SELECT * from adrval WHERE adr='{addr}'")
    ret = 0, 0
    for row in cursor:
        if DEBUG: print("> DEBUG LIB for [get_addr]",row[0], row[1])
        ret = row[0], row[1]

    return ret # first item       


def blocks_list():
    cursor = conn.execute("SELECT * from blocks")

    for row in cursor:
        print(row[0], row[1], row[3])
        print("date_time", row[2], datetime.datetime.fromtimestamp(row[2]))


def delete_all():
    if DEBUG: print("> DEBUG LIB [delete_all]")
    cursor.execute('DELETE FROM adrval')
    conn.commit()
    cursor.execute('DELETE FROM txs')
    conn.commit()


def db_close():
    conn.close()
