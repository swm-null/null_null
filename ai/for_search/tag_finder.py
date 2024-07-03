from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_milvus import Milvus
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents.base import Document
from logger import logger as lg
from typing import Optional
from database.collections import tag_store

vectorstore_for_tag=tag_store
retriever=vectorstore_for_tag.as_retriever()
prompt=PromptTemplate.from_template("""
You're the assistant who listens to your customers' requests and tells them in which tag they can find this information.

I'll give you the name of each tag, and you tell me where to find this information.
The answer is just the name of the tag, no other information.
If you can't find it, print 'No tag'.

Lists of tag: {context}
Customer's request: {query}
""")

def format_docs(docs: list[Document]):
    ret=", ".join(f"{doc.page_content}" for doc in docs)
    return ret

find_tag_id_chain = (
    {"context": retriever | format_docs, "query": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def find_tag_name(query: str) -> Optional[list[str]]:
    chain_res=find_tag_id_chain.invoke(query)
    
    if chain_res == "No tag":
        return None
    
    # TODO: improve this dumb way after change the db
    all_tags: list[Document]=vectorstore_for_tag.similarity_search("", k=10000)
    if any(chain_res==tag.page_content for tag in all_tags) == False:
        raise Exception("[TF] Failed to get tag name. result:", chain_res)
    else:
        return [chain_res]