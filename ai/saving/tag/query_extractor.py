import logging
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from ai.saving.utils.embedder import embedder
from ai.vectorstores.tag_store import tag_store, tag_collection, TAG_INDEX_NAME, TAG_CONTENT_NAME
from models.add_memo import Res_add_memo, Res_memo_tag
import random

load_dotenv()

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

vectorstore_for_tag=tag_store

class Tag(BaseModel):
    name: str = Field(description="name of tag")
    id: str = Field(description="id of tag")

class Tag_list(BaseModel):
    tags: list[Tag] = Field(description="list of tags")
    def __getitem__(self, item):
        return self.tags[item]

def format_similar_tags(tags: list[dict[str, str]]) -> str:
    return ", ".join(f"{tag['name']} (id: {tag['id']})" for tag in tags)

def get_similar_tags(query: str, id: Optional[str]) -> list[dict[str, str]]:
    similar_first_tags_res=tag_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': TAG_INDEX_NAME,
                'path': "embedding",
                'queryVector': embedder.embed_query(query),
                'numCandidates': 500,
                'limit': 10,
            }
        },
        {
            "$project": 
            {
                "_id": 1,
                TAG_CONTENT_NAME: 1,
                "parent": 1,
            }
        },
        {
            "$match": 
            {
                'parent': {'$eq': id }
            }
        }
    ])

    similar_first_tags: list[dict[str, str]]=[]
    for res in similar_first_tags_res:
        similar_first_tags.append({
            "name": res[TAG_CONTENT_NAME],
            "id": res["_id"]
        })
    
    return similar_first_tags

tags_output_parser=JsonOutputParser(pydantic_object=Tag_list)
tags_format_instructions=tags_output_parser.get_format_instructions()

def get_first_tags(query: str, formatted_tags: str) -> Tag_list:
    # TODO: multiple first tag..
    first_tags_prompt=PromptTemplate.from_template(
    """
    You're an expert at analyzing and organizing sentences.
    Given a sentence, you pick one tag if it's strongly related to an existing tag, or create a new tag if you don't think it's relevant, to help organize the sentence.
    Tags are for very big fields like economy and society.
    I'll tell you which country this sentence is used in, so you can categorize it in that country's context and generate tag in their language.

    I'll give you a sentence to analyze and a list of existing tags.

    Country: Korea
    Sentence: {query}              
    List of tags: [{tag_list}]    

    {format}
    If you create a new tag, set the id to null.
    """,
    partial_variables={
        "tag_list": formatted_tags,
        "format": tags_format_instructions
        }
    )

    first_tags_chain=(
        { "query": RunnablePassthrough() }
        | first_tags_prompt
        | llm
        | JsonOutputParser()
    )
    return first_tags_chain.invoke(query)

def get_secondary_tags(query: str, first_tag: str, formatted_tags: str) -> Tag_list:
    secondary_tags_prompt=PromptTemplate.from_template(
    """
    You're an expert at analyzing and organizing sentences.
    You know that this sentence belongs to a specific domain, and you're categorizing it within that domain.
    Given a sentence, you can choose a few tags from existing tags that is relevant to this sentence, or create a new tag.
    Don't create tags with the same name as the domain.
    
    I'll tell you which country this sentence is used in, so you can categorize it in that country's context and generate tag in their language.
    I'll give you a sentence to analyze, a list of existing tags, and the domain of sentence.

    Country: Korea
    Sentence: {query}              
    List of tags: [{tag_list}]    
    Domain: [{domain}]

    {format}
    If you create a new tag, set the id to null.
    """,
    partial_variables={
        "tag_list": formatted_tags,
        "format": tags_format_instructions,
        "domain": first_tag
        }
    )

    secondary_tags_chain=(
        { "query": RunnablePassthrough() }
        | secondary_tags_prompt
        | llm
        | JsonOutputParser()
    )
    return secondary_tags_chain.invoke(query)

# returns existing tag id list, new tag list
def query_extractor(query: str, country: str="Korea") -> tuple[list[str], list[Res_memo_tag]]:
    # return arguments
    existing_tag_ids: list[str]=[]
    new_tags: list[Res_memo_tag]=[]

    # get first tag(s)
    similar_first_tags: list[dict[str, str]]=get_similar_tags(query, None)
    formatted_similar_first_tags: str=format_similar_tags(similar_first_tags)
    logging.info(f'[QE] similar first level tags: {formatted_similar_first_tags}')

    first_tags: Tag_list=get_first_tags(query, formatted_similar_first_tags)
    logging.info(f'[QE] first level chain result: {first_tags}\nfor the query: "{query}"')

    # TODO: validation for tag ids
    for first_tag in first_tags['tags']:
        if first_tag['id'] is None: # if this tag is new
            first_tag['id']="temp_id"+str(random.randint(1, 2**64))
            new_tags.append(Res_memo_tag(
                name=first_tag['name'],
                embedding=embedder.embed_query(first_tag['name']),
                parent=None,
                id=first_tag['id'],
            ))
        else:
            existing_tag_ids.append(first_tag['id'])

    # TODO: parallelize this work
    # for each first tag, find secondary tags
    for first_tag in first_tags['tags']:
        similar_secondary_tags: list[dict[str, str]]=get_similar_tags(query, first_tag['id'])
        formatted_similar_secondary_tags: str=format_similar_tags(similar_secondary_tags)
        secondary_tags: Tag_list=get_secondary_tags(query, first_tag['name'], formatted_similar_secondary_tags)
        logging.info(f'[QE] secondary level chain result: {secondary_tags}\nfor the tag: ({first_tag["name"]}, {first_tag["id"]})\nfor the query: "{query}"')

        # TODO: validation for tag ids 
        for secondary_tag in secondary_tags['tags']:
            if secondary_tag['id'] is None:
                new_tags.append(Res_memo_tag(
                    name=secondary_tag['name'],
                    embedding=embedder.embed_query(secondary_tag['name']),
                    parent=first_tag['id'],
                    id=None,
                ))
            else:
                existing_tag_ids.append(secondary_tag['id'])
    
    return (existing_tag_ids, new_tags)
