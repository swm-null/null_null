from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents.base import Document
import logging
from typing import Optional
from ai.vectorstores.tag_store import tag_store

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

vectorstore_for_tag=tag_store
retriever=vectorstore_for_tag.as_retriever()

def format_docs(docs: list[Document]):
    ret=", ".join(f"{doc.page_content}, (id: {str(doc.metadata['_id'])})" for doc in docs)
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
    if any(tag_ids==str(tag.metadata['_id']) for tag in all_tags) == False:
        logging.error("[TF] Failed tag id validation: %s", tag_ids)
        raise HTTPException(status_code=500, headers={"TF": "Failed to get tag id."})
    else:
        logging.info("[TF] Found the tags. result: [%s]", tag_ids)
        return [tag_ids]
