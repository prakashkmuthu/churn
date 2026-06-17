import joblib
import pandas as pd

model = joblib.load("models/model.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")


def predict_churn(input_data: dict):
    df = pd.DataFrame([input_data])

    df = pd.get_dummies(df)

    df = df.reindex(columns=feature_columns, fill_value=0)

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "prediction": int(prediction),
        "churn_probability": round(float(probability), 4)
    }