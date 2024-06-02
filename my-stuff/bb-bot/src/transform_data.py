import numpy as np
import pandas as pd

def prepare_data(data):
    '''
    takes the fetched open,high,low,close,vol data for currently 9 candles, transforms it to log and min-max-scaler and reshapes it into one row with 10 backward looking candles for the MA and STD calculations. 
    '''
    
    # define pandas DF 
    cols = ['time','open', 'high', 'low', 'close','vol','vol_coin']
    df = pd.DataFrame(data["result"]["list"], columns=cols).dropna()
    
    df['time'] = df['time'].astype(int)
    
    df["time"] = pd.to_datetime(df["time"],unit="ms")
    df["day"] = df["time"].dt.day
    df["hour"] = df["time"].dt.hour

    # the 10-day moving average
    df["10MA"] = df["close"].astype('float64').mean()
    
    # Calculate the standard deviation of the closing prices over the same 20-day period
    df["10STD"] = df["close"].astype('float64').std()
    
    # volume weighted close price
    df["vwap"] = df.close.astype('float64')/df.vol.astype('float64')
    
    # Bollinger Band: 
    # simple_moving_average(20) + std x 2 | sma - std x 2
    df["bb_upper_band"] = df["10MA"].astype('float64') + 2 * df["10STD"].astype('float64')
    df["bb_lower_band"] = df["10MA"].astype('float64') - 2 * df["10STD"].astype('float64')

    # Calculate On-Balance Volume (OBV)
    df["change"] = df["close"].astype('float64').diff(periods=-1)#.shift(-1)
    df["direction"] = df["change"].astype('float64').apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    df["obv"] = df["vol"].astype('float64') * df["direction"].astype('float64')
    df["obv"] = df["obv"].astype('float64').cumsum()

    # Stack the DataFrame for all non-constant rows of the period (OHLC,vol,vwap,obv)
    stacked_df_cols = ["open","high","low","close","vol","vol_coin","vwap","obv","change","direction"]
    stacked_df = df.loc[0:len(df)-2,stacked_df_cols].stack() #cut the last row 0:8=9, (10-2) bc of diff = NAN
    
    # Create a new DataFrame from the stacked series and transpose it
    # this creates a multi index data frame with tuples as indices, like [(0,'ts'),...]
    df_single_row = stacked_df.to_frame().T
    
    # now change the multiindex col to a single index col by replacing it witht a list of concatenated strings 
    df_single_row.columns = [f'{col[1]}_{col[0]}' for col in df_single_row.columns]

    # get the first row of the bollinger band metrics that are a constant for the 10 observations
    bb_cols = ["10MA","10STD","bb_upper_band","bb_lower_band"]
    df_bb_metrics = df[bb_cols].head(1)

    # collect meta data
    meta_cols = ["day","hour"]
    df_meta = df[meta_cols].head(1)

    # put cols side by side
    df_concat = pd.concat([df_meta,df_bb_metrics,df_single_row],axis=1)
    
    return df,stacked_df,df_single_row,df_concat
    