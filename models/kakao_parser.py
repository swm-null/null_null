from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class kakao_parser_type(Enum):
    CSV="csv"
    TXT="txt"

class Arg_kakao_parser(BaseModel):
    type: kakao_parser_type
    content: str

class Res_kakao_parser(BaseModel):
    parsed_memolist: list[tuple[str, datetime]]
