# In essence the function calls would look like this: 

import * from ... 

response = fetch_kline()
pred_df = prepare_data(response)

entry,stop_loss,take_profit = make_prediction(prep_df) # add column if trade or not 

write_db(prep_df)

place_order(entry,stop_loss,take_profit)

