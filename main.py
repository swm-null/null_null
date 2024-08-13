from fastapi import FastAPI, status
import uvicorn
import logging
from init import init

from ai.utils.embedder import embedder
from ai.saving.adder.single_adder import single_adder
from ai.saving.adder.batch_adder import batch_adder
from ai.searching.regex_generator import get_regex
from ai.searching.query_analyzer import Query_Type, query_analyzer
from ai.searching.similarity_search import similarity_search
from ai.searching.tag_finder import find_tag_ids

from ai.saving.parser import kakao_parser as kp

from models.add_memo import *
from models.search import *
from models.get_embedding import *
from models.kakao_parser import *

app = FastAPI(
    title="Oatnote AI",
    description="after PR #39, added batch adder",
    version="0.1.2",
)
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

@app.post("/search/", response_model=Res_search)
async def search(body: Arg_search):
    return_content: Res_search=Res_search()

    return_content.type=query_analyzer(body.content)

    if return_content.type == Query_Type.unspecified:
        logging.info("[/search] unspecified query: %s", body.content)
        return_content.type=Query_Type.similarity

    if return_content.type == Query_Type.regex:
        return_content.regex=get_regex(body.content)

    elif return_content.type == Query_Type.tags:
        return_content.tags=find_tag_ids(body.content)
        # if the tag search result is None
        if return_content.tags == None:
            # then trying similarity search
            return_content.type=Query_Type.similarity
        
    if return_content.type == Query_Type.similarity:
        return_content.processed_message, return_content.ids=similarity_search(body.content)

    logging.info("[/search] query: %s / query type: %s \nreturn: %s", body.content, return_content.type, return_content)

    return return_content

@app.post("/add_memo/", response_model=Res_add_memo, status_code=status.HTTP_200_OK)
async def add_memo(body: Arg_add_memo):
    return single_adder(body)

@app.post("/get_embedding/", response_model=Res_get_embedding)
async def get_embedding(body: Arg_get_embedding):
    return Res_get_embedding(
        embedding=embedder.embed_query(body.content)
    )

@app.post("/kakao-parser/", response_model=list[Res_add_memo])
async def kakao_parser(body: Arg_kakao_parser):
    parsed_memolist: list[tuple[str, datetime]]=kp.kakao_parser(body.content, body.type)
    memolist: list[Arg_add_memo]=[
        Arg_add_memo(content=content, timestamp=timestamp) for content, timestamp in parsed_memolist
    ]
    
    return await batch_adder(memolist)

if __name__ == '__main__':
    uvicorn.run(app)
