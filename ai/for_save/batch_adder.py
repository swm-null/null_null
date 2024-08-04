from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from ai.for_save import query_extractor as qe
from models.add_memo import Res_add_memo, Res_memo_tag

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

async def batch_adder(memolist: list[tuple[str, datetime]]) -> list[Res_add_memo]:
    results: list[Res_add_memo]=[]

    # TODO: improve this method..
    for (content, timestamp) in memolist:
        existing_tag_ids: list[str]
        new_tags: list[Res_memo_tag]
        existing_tag_ids, new_tags = qe.query_extractor(content)

        results.append(Res_add_memo(
            memo_embeddings=embeddings.embed_query(content),
            existing_tag_ids=existing_tag_ids,
            new_tags=new_tags,
            timestamp=timestamp,
        ))
    
    return results
