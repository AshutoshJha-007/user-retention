from dataclasses import dataclass

@dataclass
class Config:
    data_path: str = "data.csv"   # placeholder
    date_cols: tuple = ("signup_date", "activity_date")
    user_col: str = "user_id"
    freq: str = "D"  # 'D' (daily) or 'M' (monthly)
    max_periods: int = 30
