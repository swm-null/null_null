from pydantic import BaseModel
from datetime import datetime

class Arg_kakao_parser(BaseModel):
    content: str

class Res_kakao_parser(BaseModel):
    parsed_memolist: list[tuple[str, datetime]]
