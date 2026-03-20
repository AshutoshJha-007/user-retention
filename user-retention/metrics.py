import pandas as pd

def summary_stats(retention: pd.DataFrame) -> pd.DataFrame:
    # compute average retention by period
    avg = retention.mean(axis=0).rename("avg_retention")
    # compute decay slope (simple difference)
    decay = avg.diff().rename("delta")
    return pd.concat([avg, decay], axis=1)
