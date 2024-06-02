import requests
import time
from pandas import Timestamp 

def fetch_kline():
    '''
    fetches data from bybit with hard-coded characteristics. 
    '''
    # Define the endpoint and parameters
    base_url = "https://api-testnet.bybit.com"
    endpoint = "/v5/market/kline"
    symbol = "BTCUSD"  # Example trading pair
    interval = "1"    # Kline interval, e.g., "1", "5", "15", "60", "240", etc.
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
