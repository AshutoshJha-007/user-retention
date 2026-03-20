# User Retention & Cohort Analysis (Production-Style)

## Overview
A modular, production-style cohort analysis toolkit to compute retention, churn, and LTV proxies.

## Features
- Clean architecture (config, io, core, metrics, viz, cli)
- Daily/Monthly cohorts
- Retention & churn matrices
- LTV proxy (optional revenue input)
- CLI for reproducible runs
- Basic tests

## Project Structure
```
user-retention-pro/
 ├── cohort/
 │   └── core.py
 ├── utils/
 │   ├── logger.py
 │   └── validation.py
 ├── tests/
 │   └── test_cohort.py
 ├── config.py
 ├── io.py
 ├── metrics.py
 ├── viz.py
 ├── cli.py
 ├── requirements.txt
 └── README.md
```

## Usage
```
pip install -r requirements.txt
python cli.py --data data.csv --freq D --max_periods 30
```

## Business Impact
- Identify early drop-offs
- Compare cohort quality over time
- Support retention strategies & LTV estimation
