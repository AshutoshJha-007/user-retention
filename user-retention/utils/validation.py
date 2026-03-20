import pandas as pd

REQUIRED_COLS = ["user_id", "signup_date", "activity_date"]

def validate_schema(df: pd.DataFrame):
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def validate_types(df: pd.DataFrame):
    # basic checks
    if df["user_id"].isnull().any():
        raise ValueError("user_id contains nulls")
