import hashlib
import hmac
import uuid
import requests
import time
import json
from pandas import Timestamp 


# DEMO NET
api_key = "GMUtVbMzRhohkOagoW"
secret_key = "vexur1jjKy5AiQE0rXMhVYbjRFRy6jVxhIhf"


def fetch_kline():
    '''
    fetches data from bybit with hard-coded characteristics (to be parametriziced). 
    '''
    # Define the endpoint and parameters
    base_url = "https://api-demo.bybit.com"
    endpoint = "/v5/market/kline"
    symbol = "BTCUSDT"  # Example trading pair
    interval = "15"    # Kline interval, e.g., "1", "5", "15", "60", "240", etc.
    limit = 10        # Number of klines to fetch
    start_time = int(time.time()) - 3600 * 24  # Start time in seconds (e.g., 24 hours ago)
    
    # Construct the URL
    url = f"{base_url}{endpoint}?category=linear&symbol={symbol}&interval={interval}&limit={limit}"#&start_time={start_time}"
    
    # Make the GET request
    response = requests.get(url,headers={}, data={})
    data = response.json() 
    
    # print(data)
    # print(Timestamp(data["time"],unit="ms"))
    return data


def genSignature(payload):
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature

def HTTP_Request(endPoint,method,payload,Info):
    global time_stamp
    httpClient=requests.Session()
    time_stamp=str(int(time.time() * 10 ** 3))
    # url = "https://api-testnet.bybit.com" # Testnet endpoint
    url = "https://api-demo.bybit.com" # DEMO endpoint
    signature=genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': str(10000),
        'Content-Type': 'application/json'
    }
    if(method=="POST"):
        response = httpClient.request(method, url+endPoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url+endPoint+"?"+payload, headers=headers)
    print(response)
    print(response.text)
    print(Info + " Elapsed Time : " + str(response.elapsed))
    return response#.json()


def active_orders(api_key,api_secret):
    endpoint="/v5/order/realtime"
    method="GET"
    params='category=linear&settleCoin=USDT'
    res = HTTP_Request(endpoint,method,params,"Position List")
    res = res.json()
    num_orders = len(res['result']['list'])
    symbols = [entry["symbol"] for entry in res['result']['list']]
    return num_orders,symbols


def active_positions(api_key,api_secret):
    endpoint="/v5/position/list"
    method="GET"
    params='category=linear&settleCoin=USDT'
    res = HTTP_Request(endpoint,method,params,"Position List")
    res = res.json()
    num_orders = len(res['result']['list'])
    symbols = [entry["symbol"] for entry in res['result']['list']]
    return num_orders,symbols

def place_order(api_key,api_secret,side,entry):#,take_profit,stop_loss):
    '''
    places an order at the bybit exchange only if there is no active order or position
    '''
    endpoint="/v5/order/create"
    method="POST"
    symbol = "BTCUSDT"
    side = "Buy" if side == "up" else "Sell"
    params={
    "category":"linear",
    "symbol": symbol,
    "side": side,
    "orderType": "Limit",
    "qty": "0.001",
    "price": entry}
    #TP
    #SL is missing
    params = json.dumps(params)
    
    # check active order
    active_positions_count, active_symbols_pos = active_positions(api_key, api_secret)
    active_orders_count, active_symbols_order = active_orders(api_key, api_secret)

    if symbol not in active_symbols_pos + active_symbols_order:
        if (active_positions_count < 1) & (active_orders_count < 1):
            res = HTTP_Request(endpoint, method, params, "Create Order")
        else: 
            res = "No order placed because of active orders or positions."
    else:
        res = "No order placed because of active Symbols."
            
    return res






