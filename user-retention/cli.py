import argparse
from config import Config
from io import load_csv
from cohort.core import CohortAnalyzer, CohortConfig
from utils.logger import get_logger
from metrics import summary_stats
from viz import plot_retention

def main():
    parser = argparse.ArgumentParser(description="Cohort Analysis CLI")
    parser.add_argument("--data", default=None, help="Path to data.csv")
    parser.add_argument("--freq", default=None, choices=["D", "M"], help="Frequency")
    parser.add_argument("--max_periods", type=int, default=None)
    args = parser.parse_args()

    cfg = Config()
    data_path = args.data or cfg.data_path
    freq = args.freq or cfg.freq
    max_p = args.max_periods or cfg.max_periods

    log = get_logger()
    log.info(f"Loading data from {data_path}")
    df = load_csv(data_path)

    analyzer = CohortAnalyzer(df, CohortConfig(freq=freq, max_periods=max_p))
    retention = analyzer.retention_matrix()
    churn = analyzer.churn_matrix()

    log.info("Retention (head):")
    print(retention.head())

    stats = summary_stats(retention)
    print("\nSummary stats:")
    print(stats.head())

    plot_retention(retention, max_periods=12)
    log.info("Saved retention_curve.png")

if __name__ == "__main__":
    main()
