from ai.for_save import single_adder as sa
from models.add_memo import Arg_add_memo, Res_add_memo

async def batch_adder(memolist: list[Arg_add_memo]) -> list[Res_add_memo]:
    results: list[Res_add_memo]=[]

    # TODO: improve this method..
    for memo in memolist:
        results.append(sa.single_adder(
            Arg_add_memo(
                content=memo.content,
                timestamp=memo.timestamp,
        )))
    
    return results
