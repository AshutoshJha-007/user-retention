import matplotlib.pyplot as plt
import pandas as pd

def plot_retention(retention: pd.DataFrame, max_periods: int = 12, title: str = "Retention Curve"):
    plt.figure()
    avg = retention.mean(axis=0).iloc[:max_periods]
    avg.plot(marker="o")
    plt.title(title)
    plt.xlabel("Period")
    plt.ylabel("Retention")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("retention_curve.png")
    plt.close()
