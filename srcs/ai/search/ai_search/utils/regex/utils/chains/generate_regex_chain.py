from operator import itemgetter
from re import Pattern
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate


class _Generate_regex_chain_input(BaseModel):
    query: str

class _Generate_regex_chain_output(BaseModel):
    regex: Pattern[str]=Field(description="regex string")

_parser = PydanticOutputParser(pydantic_object=_Generate_regex_chain_output)

_generate_regex_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You are an expert in understanding customer requests and building appropriate regex patterns.

    ### Objective:
    - Analyze the customer's request and generate a **regex pattern** following the provided guidelines and examples.

    ### Instructions:

    1. **Handling Language and Country Requirements**:
    - **Language ({lang})**: Ensure your pattern matches **syntax** or **writing conventions** typical of the specified language.  
        (For example, South Korean IDs might use Korean syntax conventions such as numeric patterns for 주민등록번호.)
    - **Country Context**: Adapt the regex to fit **common formats or patterns** used in the relevant country (e.g., national IDs, phone numbers, postal codes).
        - If the request involves a **culturally specific pattern** (like phone numbers or postal codes), ensure your regex aligns with the **standard used in that country**.

    2. **Using Examples**:
    - If examples are provided, **make the most of them** to guide your pattern design. Reference the following:
        ```
        주민등록번호: \\d{{6}}-\\d{{7}}
        전화번호: \\d{{2,3}}-\\d{{3,4}}-\\d{{4}}
        ```

    3. **Regex Constraints**:
    - **Do not use `^` or `$`** unless the customer specifically asks for a pattern that matches the **beginning** or **end** of the input.

    4. **Expected Output**:
    - Print only the **final regex pattern**—no extra text or comments.

    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_generate_regex_chain=(
    { 
        "input_json": itemgetter("input_json"),
        "lang": itemgetter("lang")
    }
    | _generate_regex_chain_prompt
    | llm4o
    | _parser
)

async def generate_regex_using_chain(query: str, lang: str) -> _Generate_regex_chain_output:
    input_json_model=_Generate_regex_chain_input(query=query)
    
    return await _generate_regex_chain.ainvoke({"input_json": input_json_model.model_dump_json(), "lang": lang})
