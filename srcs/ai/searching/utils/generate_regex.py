import logging
from re import Pattern
from ai.searching.utils.chains import generate_regex_chain


def generate_regex(query: str, lang: str="Korean") -> Pattern[str]:
    generated_regex=generate_regex_chain.invoke({"query": query, "lang": lang})
    logging.info("[generate regex]\n## %s\n\n", generated_regex.regex)
    
    return generated_regex.regex
