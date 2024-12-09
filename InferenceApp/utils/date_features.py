import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def calculate_year_features(date):
    """Calculate year sin/cos features consistently"""
    day = 24 * 60 * 60  # seconds in a day
    year = 365.2425 * day  # seconds in a year

    timestamp = pd.Timestamp(date).timestamp()
    year_sin = np.sin(timestamp * (2 * np.pi / year))
    year_cos = np.cos(timestamp * (2 * np.pi / year))

    return year_sin, year_cos


def generate_future_dates(start_date, num_days):
    """Generate a list of future dates starting from start_date."""
    return [start_date + timedelta(days=x) for x in range(num_days)]
