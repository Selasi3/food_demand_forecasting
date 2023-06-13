from fastapi import FastAPI
from models import Order
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


app = FastAPI()

scaler = StandardScaler()
le = LabelEncoder()

with open("rf_model.pkl", "rb") as file:
    rf_model = pickle.load(file)


@app.post("/predict")
def predict_amount(order:Order):
    data = pd.DataFrame({
        'Item Ordered': [order.item_ordered],
        'Quantity': [order.quantity],
        'Location': [order.location],
        'Delivery Time': [order.delivery_time],
        'Time Of Order': [order.time_of_order]
       
    })

    # Convert 'Time Of Order' column to datetime
    data['Time Of Order'] = pd.to_datetime(data['Time Of Order'], dayfirst=True)

    # Perform feature engineering
    data['Month'] = data['Time Of Order'].dt.month
    data['Day'] = data['Time Of Order'].dt.day


    # Apply LabelEncoder to categorical columns
    categorical_columns = ['Item Ordered', 'Location']
    for col in categorical_columns:
        data[col] = le.transform(data[col])

    # Scale the numerical features using the loaded scaler
    numerical_columns = ['Quantity', 'Delivery Time']
    data[numerical_columns] = scaler.transform(data[numerical_columns])
    data.drop(axis=1,columns=["Time Of Order"],inplace=True)
    # Make the prediction using the loaded RandomForestRegressor model
    amount_pred = rf_model.predict(data)[0]
    # Return the prediction result
    return {"predicted_amount": amount_pred}
