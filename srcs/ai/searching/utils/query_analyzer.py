import logging
from models.search import Search_query_type
from ai.searching.utils.chains import query_analyzer_chain

async def query_analyzer(query: str, lang: str="Korean") -> Search_query_type:
    analyzed_result=await query_analyzer_chain.ainvoke({"query": query, "lang": lang})
    logging.info("[query analyzer]\n## %s for %s\n\n", query, analyzed_result.type)
    
    return analyzed_result.type
    
