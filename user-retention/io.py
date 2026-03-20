import pandas as pd
from utils.validation import validate_schema, validate_types

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    validate_schema(df)
    validate_types(df)
    return df
