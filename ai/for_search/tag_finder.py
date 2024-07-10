from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents.base import Document
import logging
from typing import Optional
from database.collections import tag_store

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

vectorstore_for_tag=tag_store
retriever=vectorstore_for_tag.as_retriever()

def format_docs(docs: list[Document]):
    ret=", ".join(f"{doc.page_content}, (id: {doc.metadata['_id']['$oid']})" for doc in docs)
    return ret

def find_tag_ids(query: str) -> Optional[list[str]]:
    # TODO: this prompt gets only one id now
    prompt=PromptTemplate.from_template("""
    You're the assistant who listens to your customers' requests and tells them in which tag they can find this information.

    I'll give you the name of each tag, and you tell me where to find this information.
    The answer is just the id of the tag, no other information.
    If you can't find it, print 'No tag'.

    Lists of tag: {context}
    Customer's request: {query}
    """)

    find_tag_ids_chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    tag_ids=find_tag_ids_chain.invoke(query)

    if tag_ids.strip() == "No tag":
        logging.info("[TF] No tags found.")
        return None
    
    # TODO: improve this dumb way after change the db
    all_tags: list[Document]=vectorstore_for_tag.similarity_search("", k=1000)
    if any(tag_ids==str(tag.metadata['_id']['$oid']) for tag in all_tags) == False:
        raise Exception("[TF] Failed to get tag ids. result:", tag_ids)
    else:
        logging.info("[TF] Found the tags. result: [%s]", tag_ids)
        return [tag_ids]
    
# deprecated function
def find_tag_name(query: str) -> Optional[list[str]]:
    prompt=PromptTemplate.from_template("""
    You're the assistant who listens to your customers' requests and tells them in which tag they can find this information.

    I'll give you the name of each tag, and you tell me where to find this information.
    The answer is just the name of the tag, no other information.
    If you can't find it, print 'No tag'.

    Lists of tag: {context}
    Customer's request: {query}
    """)

    find_tag_name_chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    chain_res=find_tag_name_chain.invoke(query)
    
    if chain_res == "No tag":
        return None
    
    # TODO: improve this dumb way after change the db
    all_tags: list[Document]=vectorstore_for_tag.similarity_search("", k=1000)
    if any(chain_res==tag.page_content for tag in all_tags) == False:
        raise Exception("[TF] Failed to get tag name. result:", chain_res)
    else:
        return [chain_res]
