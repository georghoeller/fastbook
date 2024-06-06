from time import ctime
from src.bybit import fetch_kline
from src.transform_data import prepare_data
from src.model import predict
from src.messenger import run_send_msg
print("import done")

response = fetch_kline()
print(response)

df,stacked_df,df_single_row,df_concat = prepare_data(response)
print(df_concat)

prediction,entry,take_profit,stop_loss = predict(df_concat) 


#if prediction != "null":
    #place_order(entry,stop_loss,take_profit)

msg = f"timestamp: {ctime()} \n prediction: {prediction[0]} \n entry: {entry} \n stop_loss: {stop_loss} \n take_profit: {take_profit}"

print(msg)
run_send_msg(msg)
