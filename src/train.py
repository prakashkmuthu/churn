import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# ==========================
# MLflow Setup
# ==========================
mlflow.set_experiment("Customer Churn Prediction")

# ==========================
# Read Dataset
# ==========================
df = pd.read_csv("data/churn.csv")

# ==========================
# Basic Cleaning
# ==========================
df = df.drop("customerID", axis=1)

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df = df.dropna()

# ==========================
# Target Encoding
# ==========================
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# ==========================
# One Hot Encoding
# ==========================
df = pd.get_dummies(df, drop_first=True)

# ==========================
# Features and Target
# ==========================
X = df.drop("Churn", axis=1)
y = df["Churn"]

# ==========================
# Train Test Split
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================
# Model Parameters
# ==========================
n_estimators = 100
max_depth = 5

model = RandomForestClassifier(
    n_estimators=n_estimators,
    max_depth=max_depth,
    random_state=42
)

# ==========================
# MLflow Run
# ==========================
with mlflow.start_run(run_name="Random Forest Baseline"):

    # Model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )

    # Train
    model.fit(X_train, y_train)

    # Predict for evaluation
    y_pred = model.predict(X_test)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Print results
    print("\nAccuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    print("\nConfusion Matrix")
    print(confusion_matrix(y_test, y_pred))

    # Log parameters
    mlflow.log_param("model", "RandomForest")
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("test_size", 0.20)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("encoding", "pd.get_dummies_drop_first")

    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)

    # Save model locally
    joblib.dump(model, "models/model.pkl")

    # Log model in MLflow
    mlflow.sklearn.log_model(
        model,
        artifact_path="model"
    )

    print("\nModel saved successfully.")
    print("MLflow run logged successfully.")