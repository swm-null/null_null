import openai
from dotenv import load_dotenv
from enum import Enum
from typing import Literal
from logger import logger as lg

load_dotenv()

class Query_Type(Enum):
    regex = "regex"
    tags = "tags"
    similarity = "similarity"
    unspecified = "unspecified"

def query_analyzer(query: str) -> Query_Type:
    res=openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                You need to analyze the sentence to figure out what the user wants.
                Analyze the sentence according to the following rules and print ONE correct answer.
                Apply the rules in the order they are written, and if any of them are correct, print them out.

                -- Rules -- 
                If the sentence is a request to find information that fits a specific pattern, print 'regex'.
                If you're asking to find tags related to a specific field, print 'tags'.
                If the sentence asks to find something, print 'similarity'.
                If none of the above is true, print 'unspecified'.
            """},
            {"role": "user", "content": query}
        ],
    )

    lg.logger.info("[QA] analyzed query type: %s", res.choices[0].message.content)

    ret=res.choices[0].message.content

    if ret not in Query_Type._member_names_:
        raise Exception("Failed to analyze the query. result:", ret)
    
    return Query_Type(ret)
