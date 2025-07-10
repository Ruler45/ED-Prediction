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
    with open("models/HardnessModel1.pkl", "rb") as f:
        model1 = pickle.load(f)
    with open("models/HardnessModel2.pkl", "rb") as f:
        model2 = pickle.load(f)
    with open("models/HardnessModel3.pkl", "rb") as f:
        model3 = pickle.load(f)
    with open("models/HardnessModel4.pkl", "rb") as f:
        model4 = pickle.load(f)
    with open("models/Scaler.pkl", "rb") as f:
        scaler = pickle.load(f)


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


@app.get("/")
def root():
    return {"message": "ML Model API is running"}

@app.post("/predict")
def predict(data: InputData):
    return {"predicted_hardness": predictHardness(data),"predicted_mass_deposition": predictMassDeposition(data)}
