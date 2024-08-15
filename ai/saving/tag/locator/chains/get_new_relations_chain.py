from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.saving.tag._models.directory_relation import Directory_relation
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate


class _get_new_relations_chain_output(BaseModel):
    new_directories: list[Directory_relation]=Field(description="relations of new directory")

_parser = PydanticOutputParser(pydantic_object=_get_new_relations_chain_output)

_get_new_relations_chain_prompt=PromptTemplate.from_template(
    """
    You're an expert at categorizing files.
    Given a new directory, your job is to determine how it should be organized.
    Choose a directory based on how normal people organize their notes.

    In addition to putting new directories into existing directories, you can also create new directories of your own.
    For example, if you have an existing directory called 'plants' and you need to organize the directory 'apples', you can create a new relationship 'plants'-'apples', but also create a new directory called 'fruits', such as 'plants'-'fruits', 'fruits'-'apples', etc.

    I'm attaching the existing directory structure.
    When the number of '-'s increases, you're in that directory.
    If there's an ID next to the name, it's a directory; if there's no ID, it's a document.
    
    Language: {lang}              
    New directory: {name}
    Current directories: [
        {directories}
    ]

    {format}
    
    When you create a new directory on your own, put the name of the directory in the ID of the new directory and is_new to True.
    If you want to create a directory at the very top level, put the parent's id to null.
    """,
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

get_new_relations_chain=(
    {
        "name": itemgetter("name"),
        "lang": itemgetter("lang"),
        "directories": itemgetter("directories"),
    }
    | _get_new_relations_chain_prompt
    | llm4o
    | _parser
)
