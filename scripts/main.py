import time
from datetime import datetime
from config.settings import QUERIES
from config.logging_config import configure_logger
from core.time_utils import get_yesterday_time_range
from core.data_processor import extract_data
from core.file_handler import save_to_xlsx

logger = configure_logger()


def main():
    try:
        # Get time range (yesterday 12:00 AM to 11:59 PM EST)
        start_time, end_time = get_yesterday_time_range()
        logger.info(f"Fetching data from {start_time} to {end_time}")

        # Process each query
        for query in QUERIES:
            try:
                logger.info(f"Processing query: {query['query_name']}")
                data = extract_data(query["nrql"], start_time, end_time)

                if not data:
                    logger.warning(f"No data found for {query['query_name']}")
                else:
                    logger.info(f"Fetched {len(data)} records for {query['query_name']}")
                    file_path = save_to_xlsx(data, query["query_name"])

                    if file_path:
                        logger.info(f"Successfully saved {query['query_name']} to {file_path}")
                    else:
                        logger.error(f"Failed to save {query['query_name']}")

                time.sleep(2)  # Delay between queries

            except Exception as e:
                logger.error(f"Error processing {query['query_name']}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Fatal error in main execution: {str(e)}")
        raise


if __name__ == '__main__':
    main()