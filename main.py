from fastapi import FastAPI
from models import Order
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = FastAPI()

scaler = StandardScaler()
item_ordered_encoder = LabelEncoder()
item_ordered_encoder.fit(["A", "B", "C", "D", "E"])
pickle.dump(item_ordered_encoder, open("item_ordered_encoder.pkl", "wb"))

location_encoder = LabelEncoder()
location_encoder.fit(["Accra", "Dansoman", "East-Lagon", "Kaneshie", "Mallam"])
pickle.dump(location_encoder, open("location_encoder.pkl", "wb"))

with open("rf_model.pkl", "rb") as file:
    rf_model = pickle.load(file)

with open("location_encoder.pkl", "rb") as file:
    location_encoder = pickle.load(file)

with open("item_ordered_encoder.pkl", "rb") as file:
    item_ordered_encoder = pickle.load(file)



@app.post("/predict")
async def predict_amount(order: Order):

    
    order.item_ordered = int(item_ordered_encoder.transform([order.item_ordered])[0])
    order.location = int(location_encoder.transform([order.location])[0])

    order = [[
        order.item_ordered,
        order.quantity,
        order.location,
        order.delivery_time,
        order.month,
        order.day  # Use 'time_of_order.day' instead of 'day'
    ]]
    print(order)
    # Make the price prediction
    predicted_price = rf_model.predict(order)

    return {"predicted_price": predicted_price[0]}
