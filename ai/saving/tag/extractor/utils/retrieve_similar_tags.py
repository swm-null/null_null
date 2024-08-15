import logging
from operator import itemgetter
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from ai.saving.tag.utils.tag_formatter import tag_formatter
from ai.utils.embedder import embedder
from ai.utils.llm import llm4o
from ai.vectorstores.tag_store import TAG_CONTENT_NAME, TAG_ID_NAME, TAG_INDEX_NAME, tag_collection
from ai.saving.tag._models.tag import Tag


def retrieve_similar_tags(query: str) -> str:
    tag_list: list[Tag]=_get_similar_tags_from_db(query)
    formatted_tag_list=tag_formatter(tag_list)
    return formatted_tag_list

def _get_similar_tags_from_db(query: str) -> list[Tag]: 
    raw_tags=tag_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': TAG_INDEX_NAME,
                'path': "embedding",
                'queryVector': embedder.embed_query(query),
                'numCandidates': 1000,
                'limit': 20,
            }
        },
        {
            "$project": 
            {
                "_id": 1,
                TAG_CONTENT_NAME: 1,
                "child": 1,
            }
        },
        {
            "$match":  # only leaf tags
            {
                "$expr": { "$eq": [{ "$size": "$child" }, 0] }
            }
        }
    ])

    similar_tags: list[Tag]=[]
    
    for res in raw_tags:
        similar_tags.append(Tag(
            id=str(res[TAG_ID_NAME]),
            name=res[TAG_CONTENT_NAME],
        ))
    return similar_tags
