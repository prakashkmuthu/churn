from fastapi import FastAPI
from src.predict import predict_churn

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Customer Churn API is running"}


@app.post("/predict")
def predict(data: dict):
    result = predict_churn(data)
    return result