import requests
import time
import pandas as pd
import numpy as np

def fetch_data():
    '''
    fetches data from bybit with hard-coded characteristics. 
    '''
    # Define the endpoint and parameters
    base_url = "https://api-testnet.bybit.com"
    endpoint = "/v5/market/kline"
    symbol = "BTCUSD"  # Example trading pair
    interval = "1"    # Kline interval, e.g., "1", "5", "15", "60", "240", etc.
    limit = 4        # Number of klines to fetch
    start_time = int(time.time()) - 3600 * 24  # Start time in seconds (e.g., 24 hours ago)
    
    # Construct the URL
    url = f"{base_url}{endpoint}?category=linear&symbol={symbol}&interval={interval}&limit={limit}"#&start_time={start_time}"
    
    # Make the GET request
    response = requests.get(url,headers={}, data={})
    data = response.json() 
    
    print(data)
    print(pd.Timestamp(data["time"],unit="ms"))
    return data


def prepare_data(data):
    '''
    takes the fetched open,high,low,close,vol data for 4 candles, transforms it to log and min-max-scaler and reshapes it into one row. 
    '''

    # define pandas DF 
    cols = ['ts','open', 'high', 'low', 'close','vol','vol_coin']
    df = pd.DataFrame(data["result"]["list"], columns=cols)

    # applying logs
    for col in cols:
        df["log_"+str(col)] = np.log(df[str(col)].astype('float64')+1)

    # >>> AS FOR NOW useless
    # normalize along "MinMaxScaler" (same like sci kit learn)
    # for col in cols+["log_vol"]:
    #    df["norm_"+str(col)] =  (df[str(col)].astype('float64') - np.min(df[str(col)].astype('float64')) ) / ( np.max(df[str(col)].astype('float64')) - np.min(df[str(col)].astype('float64')) ) 

    # Stack the DataFrame
    stacked_df = df.stack()
    
    # Create a new DataFrame from the stacked series and transpose it
    # this creates a multi index data frame with tuples as indices, like [(0,'ts'),...]
    df_single_row = stacked_df.to_frame().T
    
    # now change the multiindex col to a single index col by replacing it witht a list of concatenated strings 
    df_single_row.columns = [f'{col[1]}_{col[0]}' for col in df_single_row.columns]
    
    return df_single_row

def write_db(data):
    '''
    writes to an sql lite database one row of the prepared data
    '''
    prep_df = prepare_data(data) # only necessary if non prepped data is passed 
    prep_df.to_sql('BTCUSDT',engine, if_exists = 'append', index=False)


def place_order(entry,sl,tp):
    '''
    Places an order along entry, sl, tp with fixed take profit as predicet with the model. 
    '''
    return None
