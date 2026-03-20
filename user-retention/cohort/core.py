from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class CohortConfig:
    user_col: str = "user_id"
    signup_col: str = "signup_date"
    activity_col: str = "activity_date"
    freq: str = "D"  # 'D' or 'M'
    max_periods: int = 30

class CohortAnalyzer:
    def __init__(self, df: pd.DataFrame, cfg: CohortConfig):
        self.df = df.copy()
        self.cfg = cfg
        self._prepare()

    def _prepare(self):
        self.df[self.cfg.signup_col] = pd.to_datetime(self.df[self.cfg.signup_col])
        self.df[self.cfg.activity_col] = pd.to_datetime(self.df[self.cfg.activity_col])

        # normalize to period (daily/monthly)
        if self.cfg.freq == "M":
            self.df["cohort"] = self.df.groupby(self.cfg.user_col)[self.cfg.signup_col].transform("min").dt.to_period("M").dt.to_timestamp()
            activity = self.df[self.cfg.activity_col].dt.to_period("M").dt.to_timestamp()
            cohort = self.df["cohort"]
            self.df["period_index"] = (activity.dt.to_period("M") - cohort.dt.to_period("M")).apply(lambda x: x.n)
        else:
            self.df["cohort"] = self.df.groupby(self.cfg.user_col)[self.cfg.signup_col].transform("min").dt.floor("D")
            activity = self.df[self.cfg.activity_col].dt.floor("D")
            cohort = self.df["cohort"]
            self.df["period_index"] = (activity - cohort).dt.days

        # keep only non-negative periods and cap
        self.df = self.df[(self.df["period_index"] >= 0) & (self.df["period_index"] <= self.cfg.max_periods)]

    def cohort_table(self) -> pd.DataFrame:
        table = self.df.pivot_table(
            index="cohort",
            columns="period_index",
            values=self.cfg.user_col,
            aggfunc="nunique"
        ).sort_index()
        return table

    def retention_matrix(self) -> pd.DataFrame:
        table = self.cohort_table()
        cohort_size = table.iloc[:, 0].replace(0, np.nan)
        retention = table.divide(cohort_size, axis=0)
        return retention

    def churn_matrix(self) -> pd.DataFrame:
        return 1 - self.retention_matrix()

    def ltv_proxy(self, revenue_df: pd.DataFrame, revenue_col: str = "revenue") -> pd.DataFrame:
        # revenue_df must have same keys: user_id, activity_date, revenue
        rev = revenue_df.copy()
        rev[self.cfg.activity_col] = pd.to_datetime(rev[self.cfg.activity_col])
        merged = self.df.merge(rev[[self.cfg.user_col, self.cfg.activity_col, revenue_col]],
                               on=[self.cfg.user_col, self.cfg.activity_col],
                               how="left")
        merged[revenue_col] = merged[revenue_col].fillna(0.0)

        if self.cfg.freq == "M":
            period = merged[self.cfg.activity_col].dt.to_period("M").dt.to_timestamp()
            cohort = merged["cohort"].dt.to_period("M").dt.to_timestamp()
            merged["period_index"] = (period.dt.to_period("M") - cohort.dt.to_period("M")).apply(lambda x: x.n)
        else:
            merged["period_index"] = (merged[self.cfg.activity_col].dt.floor("D") - merged["cohort"]).dt.days

        merged = merged[(merged["period_index"] >= 0) & (merged["period_index"] <= self.cfg.max_periods)]

        ltv = merged.pivot_table(
            index="cohort",
            columns="period_index",
            values=revenue_col,
            aggfunc="sum"
        ).sort_index()

        cohort_size = self.cohort_table().iloc[:, 0].replace(0, np.nan)
        ltv_per_user = ltv.divide(cohort_size, axis=0)
        return ltv_per_user.cumsum(axis=1)
