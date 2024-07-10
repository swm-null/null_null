import openai
import os
import logging
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_milvus import Milvus
from langchain_core.prompts import PromptTemplate
from langchain_core.documents.base import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from database.collections import tag_store
from operator import itemgetter

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

vectorstore_for_tag=tag_store
# one level extractor
prompt=PromptTemplate.from_template("""
You're an expert at analyzing and organizing sentences.
Given a sentence, you pick a tag if it's strongly related to an existing tag, or create a new tag if you don't think it's relevant, to help organize the sentence.
Tags are for big fields like economy and society.
I'll tell you which country this sentence is used in, so you can categorize it in that country's context and generate tag in their language.

I'll give you a sentence to analyze and a list of existing tags.
Return only the tag name.

Country: Korea
Sentence: {query}              
List of tags: {tag_list}                       
""")

def format_contexts(docs: list[Document]) -> str:
    return ", ".join(f"{doc.page_content} (id: {doc.metadata['pk']})" for doc in docs)


retriever=vectorstore_for_tag.as_retriever(kwargs={"k": 10})
one_level_chain=(
    {
        "query": RunnablePassthrough(),
        "tag_list": retriever | format_contexts, # get the existing similar tags from db using embedding search
    }
    | prompt
    | llm
    | StrOutputParser()
)

# [(tag_name, tag_id)...]
def query_extractor(query: str, country: str="Korea") -> list[tuple[str, str]]:
    chain_res: str=one_level_chain.invoke(query)
    logging.info(f'[QE] chain result: {chain_res} for "{query}"')

    # check whether the tag in the database
    # TODO: use the database directly without embedding search
    search_res: list[Document]=vectorstore_for_tag.similarity_search(chain_res, 1)

    # add a new tag
    if len(search_res)==0 or search_res[0].page_content != chain_res:
        insert_res: str=vectorstore_for_tag.add_texts([chain_res])[0] # get the new _id
        logging.info(f'[QE] added new tag: {chain_res} / {insert_res} for "{query}"')
        return [(chain_res, insert_res)]

    # use existing tag
    else: 
        found_res: list[str]
        logging.info(f"[QE] found the tag: {search_res[0].page_content} / {search_res[0].metadata['_id']['$oid']} for '{query}'")
        return [(chain_res, search_res[0].metadata['_id']['$oid'])]
