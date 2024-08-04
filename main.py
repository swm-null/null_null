from fastapi import FastAPI, status
import uvicorn
import logging

from init import init

from ai.for_search import query_analyzer as qa
from ai.for_search import regex_generator as rg
from ai.for_search import tag_finder as tf
from ai.for_search import similarity_search as ss
from ai.for_save import query_extractor as qe
from ai.for_save import kakao_parser as kp
from ai.for_save import batch_adder as ba

from models.add_memo import *
from models.search import *
from models.get_embedding import *
from models.kakao_parser import *

app = FastAPI(
    title="Oatnote AI",
    description="after PR #36",
    version="0.1.1",
)
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

@app.post("/search/", response_model=Res_search)
async def search(body: Arg_search):
    return_content: Res_search=Res_search()

    return_content.type=qa.query_analyzer(body.content)

    if return_content.type == qa.Query_Type.unspecified:
        logging.info("[/search] unspecified query: %s", body.content)
        return_content.type=qa.Query_Type.similarity

    if return_content.type == qa.Query_Type.regex:
        return_content.regex=rg.get_regex(body.content)

    elif return_content.type == qa.Query_Type.tags:
        return_content.tags=tf.find_tag_ids(body.content)
        # if the tag search result is None
        if return_content.tags == None:
            # then trying similarity search
            return_content.type=qa.Query_Type.similarity
        
    if return_content.type == qa.Query_Type.similarity:
        return_content.processed_message, return_content.ids=ss.similarity_search(body.content)

    logging.info("[/search] query: %s / query type: %s \nreturn: %s", body.content, return_content.type, return_content)

    return return_content

@app.post("/add_memo/", response_model=Res_add_memo, status_code=status.HTTP_200_OK)
async def add_memo(body: Arg_add_memo):
    existing_tag_ids: list[str]
    new_tags: list[Res_memo_tag]
    existing_tag_ids, new_tags = qe.query_extractor(body.content)

    return Res_add_memo(
        memo_embeddings=qe.embeddings.embed_query(body.content),
        existing_tag_ids=existing_tag_ids,
        new_tags=new_tags,
        timestamp=datetime.now()
    )

@app.post("/get_embedding/", response_model=Res_get_embedding)
async def get_embedding(body: Arg_get_embedding):
    return Res_get_embedding(
        embedding=qe.embeddings.embed_query(body.content)
    )

@app.post("/kakao-parser/", response_model=list[Res_add_memo])
async def kakao_parser(body: Arg_kakao_parser):
    parsed_memolist=kp.kakao_parser(body.content, body.type)
    results: list[Res_add_memo]=await ba.batch_adder(parsed_memolist)
    
    return results

if __name__ == '__main__':
    uvicorn.run(app)
