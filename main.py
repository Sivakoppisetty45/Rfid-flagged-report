import time
from RFID_flagged_products_Email_Report.config.settings import QUERIES
from RFID_flagged_products_Email_Report.config.logging_config import configure_logging
from RFID_flagged_products_Email_Report.core.time_utils import get_yesterday_time_range
from RFID_flagged_products_Email_Report.core.data_processor import extract_data
from RFID_flagged_products_Email_Report.core.file_handler import save_to_xlsx

logger = configure_logging()


def main():
    try:
        # Get time range (yesterday 12:00 AM to 11:59 PM EST)
        start_time, end_time = get_yesterday_time_range()
        logger.info(f"Fetching data from {start_time} to {end_time}")

        # Process each query
        for query in QUERIES:
            query_name = query['query_name']  # Moved outside try block
            try:
                logger.info(f"Processing query: {query_name}")

                data = extract_data(query["nrql"], start_time, end_time)

                if not data:
                    logger.warning(f"No data found for {query_name}")
                    print(f"No data found for {query_name}")
                else:
                    print(f"Total events fetched for {query_name}: {len(data)}")
                    file_path = save_to_xlsx(data, query_name)

                    if file_path:
                        logger.info(f"Successfully saved {query_name} to {file_path}")
                    else:
                        logger.error(f"Failed to save {query_name}")

                time.sleep(2)  # Delay between queries

            except Exception as e:
                logger.error(f"Error processing {query_name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Fatal error in main execution: {str(e)}")
        raise


if __name__ == '__main__':
    main()