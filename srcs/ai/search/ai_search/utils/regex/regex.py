from re import Pattern
from ai.search.ai_search.utils.regex.utils import generate_regex


async def regex(query: str, lang: str="Korean") -> Pattern[str]:
    generated_regex: Pattern[str]=await generate_regex(query, lang)
    
    return generated_regex
