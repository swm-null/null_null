import csv
from enum import Enum
from io import StringIO
from datetime import datetime

def kakao_parser(content: str) -> list[tuple[str, datetime]]:
    csv_reader: csv.DictReader=_get_csv_reader_from_string(content)
    parsed_memolist: list[tuple[str, datetime]]=_parse_csv_reader(csv_reader)
    unique_parsed_memolist: list[tuple[str, datetime]]=_remove_duplicated_memos(parsed_memolist)

    return unique_parsed_memolist

def _get_csv_reader_from_string(content: str) -> csv.DictReader:
    virtual_csv_file=StringIO(content)
    return csv.DictReader(virtual_csv_file, delimiter=',')

class _field(Enum):
    date="Date"
    user="User"
    message="Message"

def _parse_csv_reader(reader: csv.DictReader) -> list[tuple[str, datetime]]:
    result: list[tuple[str, datetime]]=[]

    time_format="%Y.%m.%d %H:%M"
    for message in reader:
        content: str=message[_field.message.value]
        date_str: str=message[_field.date.value]

        result.append((
            content,
            datetime.strptime(date_str, time_format)
        ))

    return result

def _remove_duplicated_memos(memolist: list[tuple[str, datetime]]) -> list[tuple[str, datetime]]:
    unique_memos_dict: dict[str, datetime]={}

    for message, date in memolist:
        if message not in unique_memos_dict:
            unique_memos_dict[message]=date
    
    unique_memos_list=list(unique_memos_dict.items())
    return unique_memos_list
