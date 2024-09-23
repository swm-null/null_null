from datetime import datetime
from models.memo_structures import Memos_memo_and_tags
from ai.saving.structure.models import Tag, Memo


def convert_memos_and_tags(memos_and_tags: list[Memos_memo_and_tags]) -> tuple[dict[int, Memo], list[Tag]]:
    memos: dict[int, Memo]={}
    tags: list[Tag]=[]
    
    memo_id: int=1
    for memo_and_tags in memos_and_tags:
        memos[memo_id]=Memo(content=memo_and_tags.content, timestamp=datetime.now())
        for tag in memo_and_tags.tags:
            tags.append(Tag(
                id=tag.id,
                name=tag.name,
                is_new=tag.is_new,
                connected_memo_id=memo_id
            ))        
        memo_id+=1
    
    return memos, tags
