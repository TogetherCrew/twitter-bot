from datetime import datetime, timedelta, timezone

def get_x_days_ago_UTC_timestamp(x: int):
    x_days_ago_timestamp = int((datetime.now(tz=timezone.utc) - timedelta(days=x)).timestamp() * 1000)
    return x_days_ago_timestamp
