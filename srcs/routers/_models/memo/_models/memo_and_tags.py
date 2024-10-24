from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from routers._models.memo._models.tag_name_and_id import Memo_tag_name_and_id


class Memo_memo_and_tags(BaseModel):
    content: str=Field(examples=["치즈라면 레시피: 라면 위에 치즈를 얹어 내놓는 음식으로 제조법 또한 간단하여 그냥 라면을 끓인 후 시중에 판매되는 슬라이스 체다치즈를 얹는 것으로 완성."])
    image_urls: list[str]=[]
    timestamp: Optional[datetime]=None
    tags: list[Memo_tag_name_and_id] 
