import csv
from enum import Enum
from io import StringIO
from datetime import datetime
import logging
import re
from fastapi import HTTPException
from models.kakao_parser import kakao_parser_type
from typing import Optional
from urllib.request import urlopen
from urllib.parse import quote

def kakao_parser(content: str, type: kakao_parser_type) -> list[tuple[str, datetime]]:
    parsed_memolist: list[tuple[str, datetime]]
    
    parsed_content=_parse_from_url(content)
    
    if type == kakao_parser_type.CSV:
        csv_reader: csv.DictReader=_get_csv_reader_from_string(parsed_content)
        parsed_memolist: list[tuple[str, datetime]]=_parse_csv_reader(csv_reader)    
    elif type == kakao_parser_type.TXT:
        parsed_memolist: list[tuple[str, datetime]]=_parse_txt_string(parsed_content)
    else:
        logging.error("[KP] invalid content type: %s", type)
        raise HTTPException(status_code=500, headers={"KP": "invalid content type"})

    unique_parsed_memolist: list[tuple[str, datetime]]=_remove_duplicated_memos(parsed_memolist)
    return unique_parsed_memolist

def _parse_from_url(url: str) -> str:
    encoded_url = quote(url, safe=':/')
    data: str=urlopen(encoded_url).read().decode('utf-8', 'ignore')
    data=data.replace("\ufeff", "")
    
    return data
    
def _get_csv_reader_from_string(content: str) -> csv.DictReader:
    virtual_csv_file=StringIO(content)
    return csv.DictReader(virtual_csv_file, delimiter=',')

def _parse_csv_reader(reader: csv.DictReader) -> list[tuple[str, datetime]]:
    result: list[tuple[str, datetime]]=[]

    class _csv_field(Enum):
        date="Date"
        user="User"
        message="Message"

    # time_format="%Y.%m.%d %H:%M"
    time_format="%Y-%m-%d %H:%M:%S"
    for message in reader:
        content: str=message[_csv_field.message.value]
        date_str: str=message[_csv_field.date.value]

        result.append((
            content,
            datetime.strptime(date_str, time_format)
        ))

    return result

def _parse_txt_string(original_content: str) -> list[tuple[str, datetime]]:
    result: list[tuple[str, datetime]]=[]

    # TODO: add english parser
    message_separator: re.Pattern=re.compile(r'(\d{4}년 \d{1,2}월 \d{1,2}일 \S{2} \d{1,2}:\d{2})') 
    splitted_messages: list[str]=message_separator.split(original_content)

    for i in range(1, len(splitted_messages), 2):
        date_str: str=splitted_messages[i].strip()
        message: str=splitted_messages[i+1].strip()

        parsed_message: Optional[tuple[str, datetime]]=_parse_txt_message(date_str, message)

        if parsed_message is not None:
            result.append(parsed_message)
    
    return result

def _parse_txt_message(date_str: str, message: str) -> Optional[tuple[str, datetime]]:
    # TODO: add english parser
    time_format="%Y년 %m월 %d일 %p %I:%M"
    sender_separator: re.Pattern=re.compile(r'^, (\S+)\s?:\s?(.*)', re.DOTALL)

    processed_data_str: str=date_str.replace(u'오전', 'am').replace(u'오후', 'pm') 

    match=sender_separator.match(message)
    if match:
        sender, content=match.groups()
        return (content, datetime.strptime(processed_data_str, time_format))
    
    return None


def _remove_duplicated_memos(memolist: list[tuple[str, datetime]]) -> list[tuple[str, datetime]]:
    unique_memos_dict: dict[str, datetime]={}

    for message, date in memolist:
        if message not in unique_memos_dict:
            unique_memos_dict[message]=date
    
    unique_memos_list=list(unique_memos_dict.items())
    return unique_memos_list
