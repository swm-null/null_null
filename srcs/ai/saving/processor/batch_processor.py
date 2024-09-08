from ai.saving.processor.single_processor import single_processor, single_adder_deprecated
from models.add_memo import Arg_add_memo, Res_add_memo
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

async def batch_adder_deprecated(memos: list[Arg_add_memo]) -> list[Res_add_memo]:
    results: list[Res_add_memo]=[]

    # TODO: improve this method..
    for memo in memos:
        results.append(single_adder_deprecated(
            Arg_add_memo(
                content=memo.content,
                timestamp=memo.timestamp,
        )))
    
    return results
