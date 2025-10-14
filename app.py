from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
# from sklearn.preprocessing import StandardScaler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define request schema
class InputData(BaseModel):
    Current: float
    pH: float
    Temp: float
    Bath_conc: float
    Speed: float


def predictHardness(data: InputData):

    # Load the model
    with open("models/hardness_bundle.pkl", "rb") as f:
        bundle = pickle.load(f)

    scaler = bundle["scaler"]
    model1 = bundle["model1"]
    model2 = bundle["model2"]
    model3 = bundle["model3"]
    model4 = bundle["model4"]


    input_array = np.array([
        data.Current,
        data.pH,
        data.Temp,
        data.Bath_conc,
        data.Speed
    ])
    input_array = input_array.reshape(1, -1)

    input_array = pd.DataFrame(input_array, columns=['Current ', 'pH', 'Temp', 'Bath conc.', 'Speed'])
    
    # Transform the DataFrame using the scaler
    input_array = scaler.transform(input_array)
    
    y_pred1=model1.predict(input_array)
    y_pred2=model2.predict(input_array)
    y_pred3=model3.predict(input_array)
    y_pred4=model4.predict(input_array)
    y_pred=(y_pred1+y_pred2+y_pred3+y_pred4)/4
    return y_pred[0]


def predictMassDeposition(data: InputData):
    # Load the model
    with open("models/mass_bundle.pkl", "rb") as f:
        bundle = pickle.load(f)

    scaler = bundle["scaler"]
    model1 = bundle["model1"]
    model2 = bundle["model2"]
    model3 = bundle["model3"]
    model4 = bundle["model4"]

    input_array = np.array([
        data.Current,
        data.pH,
        data.Temp,
        data.Bath_conc,
        data.Speed
    ])
    input_array = input_array.reshape(1, -1)

    input_array = pd.DataFrame(input_array, columns=['Current ', 'pH', 'Temp', 'Bath conc.', 'Speed'])
    # Transform the DataFrame using the scaler
    input_array = scaler.transform(input_array)
    
    y_pred1 = model1.predict(input_array)
    y_pred2 = model2.predict(input_array)
    y_pred3 = model3.predict(input_array)
    y_pred4 = model4.predict(input_array)
    y_pred = (y_pred1 + y_pred2 + y_pred3 + y_pred4) / 4
    return y_pred[0]

def predictSNRatio(data: InputData):
    # Load the model
    with open("models/bundle_SN_ratio.pkl", "rb") as f:
        bundle = pickle.load(f)

    scaler = bundle["scaler"]
    model1 = bundle["model1"]
    model2 = bundle["model2"]
    model3 = bundle["model3"]
    model4 = bundle["model4"]

    input_array = np.array([
        data.Current,
        data.pH,
        data.Temp,
        data.Bath_conc,
        data.Speed
    ])
    input_array = input_array.reshape(1, -1)

    input_array = pd.DataFrame(input_array, columns=['Current ', 'pH', 'Temp', 'Bath conc.', 'Speed'])
    # Transform the DataFrame using the scaler
    input_array = scaler.transform(input_array)
    
    y_pred1 = model1.predict(input_array)
    y_pred2 = model2.predict(input_array)
    y_pred3 = model3.predict(input_array)
    y_pred4 = model4.predict(input_array)
    y_pred = (y_pred1 + y_pred2 + y_pred3 + y_pred4) / 4
    return y_pred[0]

def predictVF(data: InputData):
    # Load the model
    with open("models/bundle_volume_fraction.pkl", "rb") as f:
        bundle = pickle.load(f)

    scaler = bundle["scaler"]
    model1 = bundle["model1"]
    model2 = bundle["model2"]
    model3 = bundle["model3"]
    model4 = bundle["model4"]

    input_array = np.array([
        data.Current,
        data.pH,
        data.Temp,
        data.Bath_conc,
        data.Speed
    ])
    input_array = input_array.reshape(1, -1)

    input_array = pd.DataFrame(input_array, columns=['Current ', 'pH', 'Temp', 'Bath conc.', 'Speed'])
    # Transform the DataFrame using the scaler
    input_array = scaler.transform(input_array)
    
    y_pred1 = model1.predict(input_array)
    y_pred2 = model2.predict(input_array)
    y_pred3 = model3.predict(input_array)
    y_pred4 = model4.predict(input_array)
    y_pred = (y_pred1 + y_pred2 + y_pred3 + y_pred4) / 4
    return y_pred[0]



@app.get("/")
def root():
    return {"message": "ML Model API is running"}

@app.post("/predict")
def predict(data: InputData):
    return {
        "predicted_hardness": predictHardness(data),
        "predicted_mass_deposition": predictMassDeposition(data),
        "predicted_sn_ratio": predictSNRatio(data),
        "predicted_volume_fraction": predictVF(data)
        }
