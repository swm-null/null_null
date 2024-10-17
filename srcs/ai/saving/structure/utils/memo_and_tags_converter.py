from datetime import datetime
from models.memo import Memo_memo_and_tags
from ai.saving._models import Tag
from ai.saving.structure._models import Memo


def convert_memos_and_tags(memos_and_tags: list[Memo_memo_and_tags]) -> tuple[dict[int, Memo], list[Tag]]:
    memos: dict[int, Memo]={}
    tags: list[Tag]=[]
    now: datetime=datetime.now()
    
    memo_id: int=1
    for memo_and_tags in memos_and_tags:
        memos[memo_id]=Memo(content=memo_and_tags.content, image_urls=memo_and_tags.image_urls, timestamp=now)
        for tag in memo_and_tags.tags:
            tags.append(Tag(
                id=tag.id,
                name=tag.name,
                is_new=tag.is_new,
                connected_memo_id=memo_id
            ))
        memo_id+=1
    
    return memos, tags
