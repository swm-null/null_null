import asyncio
from routers._models.memo import Memo_memo_and_tags, Memo_processed_memo
from ai.memo.structure.deprecated.processor._models import Memo
from ai.memo.structure.deprecated.processor.utils import convert_tag, convert_relations, convert_memos_and_tags, extract_and_assign_metadata, locate_memos
from routers._models.memo import Memo_tag, Memo_tag_relation
from ai.utils import embedder


async def process_memos(user_id: str, memos_and_tags: list[Memo_memo_and_tags], lang: str="Korean") -> tuple[list[Memo_processed_memo], list[Memo_tag_relation], list[Memo_tag]]:
    memos, tags=convert_memos_and_tags(memos_and_tags)
    memos_with_metadata=await extract_and_assign_metadata(memos, lang)
    located_memos_and_tags, relations, located_tags=await locate_memos(user_id, memos_with_metadata, tags, lang)    
    
    process_memo_tasks=[asyncio.create_task(_process_memo(memo_and_tags)) for memo_and_tags in located_memos_and_tags]
    converted_relations=convert_relations(relations)
    process_tag_tasks=[asyncio.create_task(convert_tag(tag)) for tag in located_tags]
    
    processed_memos, converted_tags = await asyncio.gather(
        asyncio.gather(*process_memo_tasks),
        asyncio.gather(*process_tag_tasks)
    )
     
    return processed_memos, converted_relations, converted_tags

async def _process_memo(memo_and_tags: Memo) -> Memo_processed_memo:
    embedding_content_task=asyncio.create_task(embedder.aembed_query(memo_and_tags.content))
    embedding_metadata_task=asyncio.create_task(embedder.aembed_query(memo_and_tags.metadata))
    
    embedded_content, embedded_metadata=await asyncio.gather(embedding_content_task, embedding_metadata_task)  
    
    return Memo_processed_memo(
            content=memo_and_tags.content,
            image_urls=memo_and_tags.image_urls,
            voice_urls=memo_and_tags.voice_record_urls,
            metadata=str(memo_and_tags.metadata),
            parent_tag_ids=memo_and_tags.parent_tag_ids,
            timestamp=memo_and_tags.timestamp,
            embedding=embedded_content if memo_and_tags.content!="" else [],
            embedding_metadata=embedded_metadata if memo_and_tags.metadata!="" else []
    )
