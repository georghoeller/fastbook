import pickle 

# Load the model from the file
# with open('xgboost_model.pkl', 'rb') as file:
#     model = pickle.load(file)

def predict(data):
    model = pickle.load(open('src/xgboost_model.pkl' , 'rb'))
    prediction = model.predict(data)

    entry = None
    take_profit = None
    stop_loss = None
    print(data["bb_lower_band"])
    
    if predict == "null": 
        entry = data["bb_lower_band"]
        take_profit = data["bb_lower_band"] * 1.002
        stop_loss = data["bb_lower_band"] / 1.002
    
    if predict == "up": 
        entry = data["bb_upper_band"]
        take_profit = data["bb_upper_band"] / 1.002
        stop_loss = data["bb_upper_band"] * 1.002
    
        
    return prediction,entry,take_profit,stop_loss