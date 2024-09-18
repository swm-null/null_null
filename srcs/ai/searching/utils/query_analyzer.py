import logging
from ai.searching.models.query_type import Query_Type
from ai.searching.utils.chains.query_analyzer_chain import query_analyzer_chain

def analyzer(query: str, lang: str="Korean") -> Query_Type:
    analyzed_result=query_analyzer_chain.invoke({"query": query, "lang": lang})
    logging.info("[query analyzer]\n## %s for %s\n\n", query, analyzed_result.type)
    
    return analyzed_result.type
    
