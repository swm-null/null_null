from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_milvus import Milvus
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.documents.base import Document

# just examples -------------
memos=[
    "CBO는 미국의 국가부채 비율이 현재 96%에서 2030년까지 106%에 이르며 제2차 세계대전 때보다 높아질 것으로 예상했다.", 
    "국내총생산(GDP) 대비 미국의 국가부채 비율은 30년 후 166%에 이를 것으로 전망된다.", 
    "미국 정부의 누적 부채 규모는 34조7000억 달러 수준이다.",
    "점유란 물건에 대한 사실상의 지배상태를 의미하며 직접점유와 간접점유로 나뉜다. 피아노, 금반지, 가방 등과 같은 대부분의 동산의 소유권을 공시하는 기능을 수행한다.", 
    "소유란 어떤 물건을 사용, 수익, 처분할 수 있는 권리를 가진 상태이다.", 
    "직접점유는 물건을 빌려쓰거나 보관하고 있는 것을 포함하여 물건을 물리적으로 지배하는 상태를 말한다.", 
    "반환청구권은 물건을 빌려쓰거나 보관하는 사람에게 그 물건의 반환을 청구할 수 있는 권리이다.",
    "간접점유는 반환청구권을 가진 상태이다.",
]
memo_id=[str(x+100) for x in range(len(memos))]
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
vectorstore=Milvus.from_texts(
    texts=memos,
    embedding=embeddings,
    connection_args={
        "uri": MILVUS_URI,
    },
    ids=memo_id
)
retriever=vectorstore.as_retriever(kwargs={"k": 10})
prompt=PromptTemplate.from_template("""
You're an assistant who finds notes that have what the user asked for.

I'll give you candidate notes that might be the right answer. Then you find the note that contains the user's request among these candidates.
There can be multiple correct answers, not just one, and you return the 'id' of each note.

Memos: {context}
Customer's question: {query} 

{format_instructions}                                    
""")

def format_contexts(docs: list[Document]):
    ret=", ".join(f"{doc.page_content} (id: {doc.metadata['memo_id']})" for doc in docs)
    return ret

class Memo_List:
    ids: list[str]

output_parser=JsonOutputParser(pydantic_object=Memo_List)
format_instructions=output_parser.get_format_instructions()

similarity_search_chain = (
    {"context": retriever | format_contexts, "query": RunnablePassthrough(), "format_instructions": format_instructions}
    | prompt
    | llm
    | JsonOutputParser()
)

def search_similar_memos(query: str) -> list[str]:
    chain_res: Memo_List=similarity_search_chain.invoke(query)

    for id in chain_res.ids:
        if id not in memo_id:
            raise Exception("Failed to get memo ids. result:", chain_res)
    return chain_res.ids
