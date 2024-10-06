from operator import itemgetter
from re import Pattern
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate


class _generate_regex_chain_output(BaseModel):
    regex: Pattern[str]=Field(description="regex string")

_parser = PydanticOutputParser(pydantic_object=_generate_regex_chain_output)

_generate_regex_chain_prompt=PromptTemplate.from_template(
"""
You're an expert at listening to customer requests and building regexes.
If they give you an example, you make the most of it.
When you find the right answer, just print the expression.

I've included a few examples for your reference, as per request.
The customer is asking a question using {lang}. Please give an answer that suits customer's country.

Don't add ^ or $ to a pattern unless you're asking to create a regex that begins or ends with that pattern.

-- Example --
주민등록번호: \\d{{6}}-\\d{{7}}
전화번호: \\d{{2,3}}-\\d{{3,4}}-\\d{{4}}

Sentence: {query}

{format}
""",
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

generate_regex_chain=(
    {
        "lang": itemgetter("lang"),
        "query": itemgetter("query"),
    }
    | _generate_regex_chain_prompt
    | llm4o
    | _parser
)
