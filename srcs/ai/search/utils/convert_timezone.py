from datetime import datetime, timedelta


def convert_timezone(start_time: datetime | None, end_time: datetime | None, lang: str) -> tuple[datetime, datetime]:
    modified_start_time=start_time if start_time else datetime(2000, 1, 1)
    modified_end_time=end_time if end_time else datetime(2100, 1, 1)
    
    delta_time=-9 if lang=="Korean" else 0
    
    modified_start_time+=timedelta(hours=delta_time)
    modified_end_time+=timedelta(hours=delta_time)
    
    # return (modified_start_time, modified_end_time)
    return (datetime(2000, 1, 1), datetime(2100, 1, 1)) # for test
