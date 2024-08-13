from ai.saving.adder.single_adder import single_adder
from models.add_memo import Arg_add_memo, Res_add_memo

async def batch_adder(memolist: list[Arg_add_memo]) -> list[Res_add_memo]:
    results: list[Res_add_memo]=[]

    # TODO: improve this method..
    for memo in memolist:
        results.append(single_adder(
            Arg_add_memo(
                content=memo.content,
                timestamp=memo.timestamp,
        )))
    
    return results
