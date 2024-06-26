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

# just examples -------------
tags=["정치", "경제", "사회", "문화", "과학", "예술", "체육", "법률", "번호"]
tags_id=[str(x+101) for x in range(len(tags))]
# ---------------------------

load_dotenv()

MILVUS_URI=os.getenv("MILVUS_URI")
if MILVUS_URI == None:
    raise Exception("Invalid MILVUS_URI")

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")
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
    elif chain_res not in tags:
        raise Exception("Failed to get tag name. result:", chain_res)
    else:
        return [chain_res]