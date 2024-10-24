import logging
from routers._models.search import Search_query_type
from ai.search.utils.query_analyzer.chains import query_analyzer_using_chain

async def query_analyzer(query: str, lang: str="Korean") -> Search_query_type:
    analyzed_result=await query_analyzer_using_chain(query, lang)
    logging.info("[query analyzer]\n## %s for %s\n\n", query, analyzed_result.type)
    
    return analyzed_result.type
    
