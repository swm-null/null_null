from dotenv import load_dotenv
import logging
from fastapi import HTTPException
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.documents.base import Document
from langchain_core.pydantic_v1 import BaseModel, Field
from ai.vectorstores.memo_store import memo_store

load_dotenv()

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
    memos="\n".join(f"{doc.page_content} (id: {doc.metadata['_id']['$oid']})" for doc in docs)
    logging.info(f"[SS] retrived contexts: {memos}")
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

def memo_validation(memos: Memo_List) -> bool:
    # TODO: improve this dumb way after change the db
    all_memos: list[Document]=vectorstore_for_memo.similarity_search("", k=1000)

    for id in memos['memo_ids']:
        if not any(id==str(memo.metadata['_id']['$oid']) for memo in all_memos):
            logging.error("[SS] Failed memo id validation: %s", id)
            raise HTTPException(status_code=500, headers={"SS": "Failed to get memo ids."})
    return True
        
def similarity_search(query: str) -> tuple[str, list[str]]:
    similar_memos: Memo_List=similarity_search_chain.invoke(query)
    logging.info(f"[SS] Similar_memos:\n{similar_memos['memo_ids']}")
    
    memo_validation(similar_memos)

    # TODO: improve so babo approach
    all_memos: list[Document]=vectorstore_for_memo.similarity_search("", k=1000)
    generated_context: str='\n'.join(memo.page_content for memo in all_memos if str(memo.metadata['_id']['$oid']) in similar_memos['memo_ids'])
    
    logging.info("[SS] generated context:\n%s", generated_context)


    output_processing_prompt=PromptTemplate.from_template("""
    You need to find the answer to the user's question.

    I've included some notes that might help you answer it. Please make the best use of these notes.
    If it's a question you can't answer, print that you can't answer it.

    Notes: {context}
    The user's question: {query}
    """, 
    partial_variables={"context": generated_context})

    output_processing_chain={"query": RunnablePassthrough()} | output_processing_prompt | llm | StrOutputParser()
    return (output_processing_chain.invoke(query), similar_memos['memo_ids'])
