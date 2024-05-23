import pickle 

# Load the model from the file
with open('xgboost_model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict(data):
    prediction = model.predict(data)
    return prediction