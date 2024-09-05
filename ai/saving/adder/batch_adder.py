from ai.saving.adder.single_adder import single_adder, single_adder_deprecated
from models.add_memo import Arg_add_memo, Res_add_memo
from models.memos import Memos_processed_memo, Memos_raw_memo

async def batch_adder(memolist: list[Memos_raw_memo], user_id: str) -> list[Memos_processed_memo]:
    results: list[Memos_processed_memo]=[]

    # TODO: improve this method..
    for memo in memolist:
        results.append(single_adder(
            Memos_raw_memo(
                content=memo.content,
                timestamp=memo.timestamp,
            ), user_id)
        )
    
    return results

async def batch_adder_deprecated(memolist: list[Arg_add_memo]) -> list[Res_add_memo]:
    results: list[Res_add_memo]=[]

    # TODO: improve this method..
    for memo in memolist:
        results.append(single_adder_deprecated(
            Arg_add_memo(
                content=memo.content,
                timestamp=memo.timestamp,
        )))
    
    return results
