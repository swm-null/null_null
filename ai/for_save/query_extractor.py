import openai
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_milvus import Milvus
from langchain_core.prompts import PromptTemplate
from langchain_core.documents.base import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from logger import logger as lg
from database.collections import tag_store

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
# one level extractor
prompt=PromptTemplate.from_template("""
You're an expert at analyzing and organizing sentences.
Given a sentence, you pick a tag if it's strongly related to an existing tag, or create a new tag if you don't think it's relevant, to help organize the sentence.
I'll tell you which country this sentence is used in, so you can categorize it in that country's context and generate tag in their language.

I'll give you a sentence to analyze and a list of existing tags.
Return only the tag name.

Country: {country}
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
        "country": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

# [(tag_name, tag_id)...]
def query_extractor(query: str, country: str="Korea") -> list[tuple[str, str]]:
    chain_res: str=one_level_chain.invoke({"query": query, "country": country})
    lg.logger.info(f'[QE] chain result: {chain_res} for "{query}"')

    # check whether the tag in the database
    # TODO: use the database directly without embedding search
    search_res: list[Document]=vectorstore_for_tag.similarity_search(chain_res, 1)

    # add a new tag
    if len(search_res)==0 or search_res[0].page_content != chain_res:
        insert_res: str=vectorstore_for_tag.add_texts([chain_res])[0] # get the new pk
        lg.logger.info(f'[QE] added new tag: {chain_res} / {insert_res} for "{query}"')
        return [(chain_res, insert_res)]

    # use existing tag
    else: 
        found_res: list[str]
        lg.logger.info(f'[QE] found the tag: {search_res[0].page_content} / {search_res[0].metadata["pk"]} for "{query}"')
        return [(chain_res, search_res[0].metadata['pk'])]