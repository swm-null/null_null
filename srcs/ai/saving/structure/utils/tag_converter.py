from ai.saving._models.tag import Tag
from ai.utils import embedder
from models.memo.memo import Memo_tag


async def convert_tag(tag: Tag) -> Memo_tag:
    return Memo_tag(
        name=tag.name,
        id=tag.id,
        is_new=tag.is_new,
        embedding=await embedder.aembed_query(tag.name)
    )
