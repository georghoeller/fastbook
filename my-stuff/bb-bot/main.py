# In essence the function calls would look like this: 

from src.bybit import fetch_kline
from src.transform_data import prepare_data
from src.model import predict

print("import done")

response = fetch_kline()
print(response)

pred_df = prepare_data(response)
print(pred_df)

#entry,stop_loss,take_profit = make_prediction(prep_df) # add column if trade or not 
#write_db(prep_df)
#place_order(entry,stop_loss,take_profit)

