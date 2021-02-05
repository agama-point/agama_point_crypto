# blockchain and mempool api - bitcoin / bitcoin tes
# agama_point 2021/01

import requests, json

url_btcusd = "https://api.coinpaprika.com/v1/tickers/btc-bitcoin"
url_mempool_fees = "https://mempool.space/api/v1/fees/recommended"
url_get_tx_received = "https://chain.so/api/v2/get_tx_received"
url_get_address_balance = "https://chain.so/api/v2/get_address_balance"

# note: 10-20 sec. pause is required
def bitcoin_usd():
    res = requests.get(url_btcusd)
    # print(res)
    btcusd = res.json()['quotes']["USD"]["price"]
    return float(btcusd)


def btc_mempool_fees():
    res = requests.get(url_mempool_fees)
    print(res)
    res_json =  res.json()
    fastestFee = res_json['fastestFee']
    halfHourFee = res_json['halfHourFee']
    hourFee = res_json['hourFee']
    return fastestFee, halfHourFee, hourFee


def addr_info(url_coin,addr, debug=False):
    url_tx = url_get_tx_received + url_coin + addr
    url_adrbal = url_get_address_balance + url_coin + addr
    if debug: 
        print(url_tx)
        print(url_adrbal)

    res_num_txs = 0
    res_fin_bal = 0

    try:
        res = requests.get(url_tx)
        #print(res)
        res_json =  res.json()
        #print(res_json)
        res_stat =res_json['status']
        if res_stat == "success":
            #data': {'network': 'BTCTEST',
            res_netw = res_json['data']['network']
            res_txs = res_json['data']['txs']
            res_num_txs = len(res_txs)
            if debug: print("network: ", res_netw, " | txs: ", res_num_txs)
        else:
            if debug: print("status1: FALSE")
    except:
        print("url_get_tx_received.err")

    try:

        res = requests.get(url_adrbal)
        # print(res)
        res_json =  res.json()
        res_stat =res_json['status']
        if res_stat == "success":
            #data': {'network': 'BTCTEST',
            res_cb = res_json['data']['confirmed_balance']
            res_fin_bal = res_cb
            res_ucb = res_json['data']['unconfirmed_balance']
            if debug: print("balance: ", res_cb, res_ucb)

        else:
            if debug: print("status2: FALSE")
 

    except:
        print("url_get_tx_received.err")

    return res_num_txs, res_fin_bal

    #btcti = res.json()['quotes']["USD"]["price"]
    #return float(btcti)
