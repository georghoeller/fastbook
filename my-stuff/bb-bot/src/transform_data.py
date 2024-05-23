import numpy as np
import pandas as pd

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