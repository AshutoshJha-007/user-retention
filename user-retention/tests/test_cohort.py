import pandas as pd
from cohort.core import CohortAnalyzer, CohortConfig

def test_basic_retention():
    data = pd.DataFrame({
        "user_id": [1,1,2,2],
        "signup_date": ["2024-01-01","2024-01-01","2024-01-01","2024-01-01"],
        "activity_date": ["2024-01-01","2024-01-02","2024-01-01","2024-01-02"]
    })
    ca = CohortAnalyzer(data, CohortConfig())
    r = ca.retention_matrix()
    assert r.shape[0] == 1
