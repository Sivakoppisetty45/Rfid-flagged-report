import concurrent.futures
import pandas as pd
from core.api_client import fetch_data
from core.time_utils import divide_time_range
from config.logging_config import configure_logging

logger = configure_logging()

# Parallel fetching function
def fetch_data_parallel(nrql_query, time_chunks):
    """Fetch data for multiple time chunks in parallel."""
    all_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for chunk_start, chunk_end in time_chunks:
            chunk_query = f"{nrql_query} SINCE '{chunk_start.strftime('%Y-%m-%d %H:%M:%S')}' UNTIL '{chunk_end.strftime('%Y-%m-%d %H:%M:%S')}'"
            futures.append(executor.submit(fetch_data, chunk_query))  # Submit the fetch requests in parallel

        for future in concurrent.futures.as_completed(futures):
            chunk_data = future.result()
            all_data.extend(chunk_data)
            logger.info(f"Fetched {len(chunk_data)} events")
    return all_data


def extract_data(nrql_query, start_time, end_time):
    """Fetch data in chunks for the given time range using parallel fetching."""
    time_chunks = divide_time_range(start_time, end_time)  # Divide into time chunks
    all_data = fetch_data_parallel(nrql_query, time_chunks)
    return all_data

def remove_timestamp_columns(df):
    """Remove any timestamp-like columns."""
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            if df[column].max() > 1e12:
                df.drop(columns=[column], inplace=True)
                logger.info(f"Removed column with timestamp data: {column}")
    return df