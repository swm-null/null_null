from datetime import datetime
from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate


class Similarity_result_with_memo_chain_output(BaseModel):
    answerable: bool
    answer: str=Field(description="answer to the user's question")
    used_memo_ids: list[str]=Field(description="used memo ids")

_parser = PydanticOutputParser(pydantic_object=Similarity_result_with_memo_chain_output)

_similarity_result_with_memo_chain_prompt=PromptTemplate.from_template(
"""
You need to answer user questions.
Answer in the user's language.

I'm attaching some pre-written notes from the user that might help you answer this question.
If a user asks a time-related question, consider the current time and the time the note was written.

1. Determine if you can answer the user's question with the information provided.

2-1. If you can, set the field answerable True and create an answer to the user's question using the information provided and end this prompt. 
2-2. If you can't, set the field answerable False and exit.

Language: {language}
Current time: {current_time}
The user's question: {question}

Notes
[
{memo_context}    
]

{format}
If you use a memo to answer, write the ID of the memo in used_memo_ids.
""",
    partial_variables={
        "format": _parser.get_format_instructions(),
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
)

similarity_result_with_memo_chain=(
    {
        "question": itemgetter("question"),
        "memo_context": itemgetter("memo_context"),
        "language": itemgetter("language"),
    }
    | _similarity_result_with_memo_chain_prompt
    | llm4o
    | _parser
)
