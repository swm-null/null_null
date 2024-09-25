from ai.saving.processor import single_processor
from models.memo import Memo_processed_memo, Memo_raw_memo


# deprecated
async def batch_processor(memos: list[Memo_raw_memo], user_id: str) -> list[Memo_processed_memo]:
    results: list[Memo_processed_memo]=[]

    # TODO: improve this method..
    for memo in memos:
        results.append(single_processor(
            Memo_raw_memo(
                content=memo.content,
                timestamp=memo.timestamp,
            ), user_id)
        )
    
    return results
