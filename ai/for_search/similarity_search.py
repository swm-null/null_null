from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_milvus import Milvus
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.documents.base import Document
from langchain_core.pydantic_v1 import BaseModel, Field
from logger import logger as lg
from database.collections import memo_store

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

vectorstore_for_memo=memo_store
retriever=vectorstore_for_memo.as_retriever(kwargs={"k": 10})

class Memo_List(BaseModel):
    memo_ids: list[str] = Field(description="list of memo ids")
    def __getitem__(self, item):
        return self.memo_ids[item]

output_parser=JsonOutputParser(pydantic_object=Memo_List)
format_instructions=output_parser.get_format_instructions()

prompt=PromptTemplate.from_template("""
You're an assistant who finds notes that have what the user asked for.

I'll give you candidate notes that might be the right answer. Then you find the note that contains the user's request among these candidates.
There can be multiple correct answers, not just one, and you return the 'id' of each note.

Memos: [{context}]
Customer's question: {query}

{format} 
""",
partial_variables={"format": format_instructions}) 

def format_contexts(docs: list[Document]):
    memos="\n".join(f"{doc.page_content} (id: {doc.metadata['pk']})" for doc in docs)
    lg.logger.info(f"[SS] retrived contexts: {memos}")
    return memos

similarity_search_chain = (
    {
        "context": retriever | format_contexts, 
        "query": RunnablePassthrough(),
    }
    | prompt
    | llm
    | JsonOutputParser()
)

def search_similar_memos(query: str) -> list[str]:
    chain_res: Memo_List=similarity_search_chain.invoke(query)

    lg.logger.info(f"[SS] chain res: {chain_res['memo_ids']}")

    # TODO: improve this dumb way after change the db
    all_memos: list[Document]=vectorstore_for_memo.similarity_search("", k=10000)

    for id in chain_res['memo_ids']:
        if not any(id==str(memo.metadata['pk']) for memo in all_memos):
            raise Exception("[SS] Failed to get memo ids. result:", chain_res)
            
    return chain_res['memo_ids']

def process_result(query: str, selected_list: list[str]) -> str:
    # selected_list: list[str]=search_similar_memos(query)
    # TODO: improve this dumb way after change the db
    all_memos: list[Document]=vectorstore_for_memo.similarity_search("", k=10000)
    new_context='\n'.join(memo.page_content for memo in all_memos if str(memo.metadata['pk']) in selected_list)
    lg.logger.info("nl processing context:\n%s", new_context)

    output_processing_prompt=PromptTemplate.from_template("""
    You need to find the answer to the user's question.

    I've included some notes that might help you answer it. Please make the best use of these notes.
    If it's a question you can't answer, print that you can't answer it.

    Notes: {context}
    The user's question: {query}
    """, 
    partial_variables={"context": new_context})

    output_processing_chain={"query": RunnablePassthrough()} | output_processing_prompt | llm | StrOutputParser()
    
    return output_processing_chain.invoke(query)

