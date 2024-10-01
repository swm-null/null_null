import asyncio
from ai.saving.structure._models.memo import Memo
from ai.saving.structure.utils.metadata_extractor.chains.metadata_extractor_chain import metadata_extractor_chain, metadata_extractor_chain_output


async def extract_and_assign_metadata(memos: dict[int, Memo], lang: str) -> dict[int, Memo]:
    tasks=[_extract_and_assign_metadata(id, memo, lang) for id, memo in memos.items()]
    
    return dict(await asyncio.gather(*tasks))
        
async def _extract_and_assign_metadata(id: int, memo: Memo, lang: str) -> tuple[int, Memo]:
    chain_result: metadata_extractor_chain_output=await metadata_extractor_chain.ainvoke({"content": memo.content, "lang": lang})
    
    return id, Memo(
        content=memo.content,
        metadata=chain_result.metadata,
        parent_tag_ids=memo.parent_tag_ids,
        timestamp=memo.timestamp
    )
