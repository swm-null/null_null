import logging
from models.search import Search_query_type
from ai.searching.utils.chains import query_analyzer_chain

def query_analyzer(query: str, lang: str="Korean") -> Search_query_type:
    analyzed_result=query_analyzer_chain.invoke({"query": query, "lang": lang})
    logging.info("[query analyzer]\n## %s for %s\n\n", query, analyzed_result.type)
    
    return analyzed_result.type
    
