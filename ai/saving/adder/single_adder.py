from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from ai.saving.tag import query_extractor as qe
from ai.saving.utils.embedder import embedder
from models.add_memo import Arg_add_memo, Res_add_memo, Res_memo_tag

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

def single_adder(memo: Arg_add_memo) -> Res_add_memo:
    existing_tag_ids: list[str]
    new_tags: list[Res_memo_tag]
    existing_tag_ids, new_tags = qe.query_extractor(memo.content)

    return Res_add_memo(
        memo_embeddings=embedder.embed_query(memo.content),
        existing_tag_ids=existing_tag_ids,
        new_tags=new_tags,
        timestamp=datetime.now() if memo.timestamp is None else memo.timestamp,
    )
