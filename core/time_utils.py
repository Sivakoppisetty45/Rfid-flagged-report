from datetime import datetime, timedelta
import pytz

EST = pytz.timezone('US/Eastern')


def divide_time_range(start_time, end_time, chunk_size_minutes=5):
    """Divide the time range into smaller chunks"""
    time_chunks = []
    current_time = start_time
    while current_time < end_time:
        next_time = current_time + timedelta(minutes=chunk_size_minutes)
        if next_time > end_time:
            next_time = end_time
        time_chunks.append((current_time, next_time))
        current_time = next_time
    return time_chunks


def get_yesterday_time_range():
    """Calculate the time range for yesterday (12:00 AM to 11:59 PM)."""
    today = datetime.now(EST).date()
    yesterday = today - timedelta(days=1)

    start_time = datetime.combine(yesterday, datetime.min.time(), tzinfo=EST)  # 12:00 AM
    end_time = datetime.combine(yesterday, datetime.max.time(), tzinfo=EST)  # 11:59 PM

    return start_time, end_time


def convert_to_est(dt):
    """Convert datetime to EST"""
    return dt.astimezone(EST)