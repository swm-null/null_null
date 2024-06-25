import openai
import os
from dotenv import load_dotenv
from enum import Enum
from logger import logger as lg

load_dotenv()

class Query_Type(Enum):
    regex = "regex",
    find_tag = "find_tag",
    similarity_search = "similarity_search"
    unspecified = "unspecified",

def query_analyzer(query: str) -> str:
    res=openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                You need to analyze the sentence to figure out what the user wants.
                Analyze the sentence according to the following rules and print ONE correct answer.
                Apply the rules in the order they are written, and if any of them are correct, print them out.

                -- Rules -- 
                If the sentence is a request to find information that fits a specific pattern, print 'regex'
                If you're asking to find tags related to a specific field, print 'find_tag'.
                If the sentence asks to find something, print 'similarity_search'.
                If none of the above is true, print 'unspecified'.
            """},
            {"role": "user", "content": query}
        ],
    )
    ret=str(res.choices[0].message.content)

    if ret not in Query_Type.__members__.keys():
        raise Exception("Failed to analyze the query. result:", ret)
    
    return ret