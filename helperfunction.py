import pandas as pd

# Helper function to parse dates with different formats
def parse_dates(date_series):
    for date_format in ['%d/%m/%Y']:
        try:
            return pd.to_datetime(date_series, format=date_format, errors='coerce')
        except ValueError:
            continue
    return pd.to_datetime(date_series, errors='coerce')

