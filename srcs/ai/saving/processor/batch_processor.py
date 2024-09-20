from ai.saving.processor import single_processor
from models.memos import Memos_processed_memo, Memos_raw_memo


async def batch_processor(memos: list[Memos_raw_memo], user_id: str) -> list[Memos_processed_memo]:
    results: list[Memos_processed_memo]=[]

    # TODO: improve this method..
    for memo in memos:
        results.append(single_processor(
            Memos_raw_memo(
                content=memo.content,
                timestamp=memo.timestamp,
            ), user_id)
        )
    
    return results
