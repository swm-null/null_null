from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.saving.structure._models.directory_relation import Directory_relation
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate


class Get_new_relations_and_tags_chain_output(BaseModel):
    relations: list[Directory_relation]=Field(description="relations of new directory")
    new_directories: list[str]=Field(description="name of given directories or a newly created directory")

_parser = PydanticOutputParser(pydantic_object=Get_new_relations_and_tags_chain_output)

_get_new_relations_and_tags_chain_prompt=PromptTemplate.from_template(
"""
You're an expert at categorizing files.
Given a new directory, your job is to determine how it should be organized.
Choose a directory based on how normal people organize their notes.
You can use the directory's metadata to categorize it correctly.

In addition to putting new directories into existing directories, you can also create new directories of your own.
For example, if you have an existing directory called 'plants' and you need to organize the directory 'apples', you can create a new relationship 'plants'-'apples', but also create a new directory called 'fruits', such as 'plants'-'fruits', 'fruits'-'apples', etc.
However, do not create a new tag with the same name as an existing tag.
If you created a new directory, make sure the name and ID of that directory are exactly the same.

I'm attaching the existing directory structure.
The directory with the name '@' is the root.
A string next to the name is the directory's id.
When the number of '-'s increases, it means you're inside that directory.
Write the directory's name in the user's language.

Language: {lang}
New directories: {tags}
Memos' metadatas: {metadatas}

Current directories: [
{directories}
]

{format}
""",
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

get_new_relations_and_tags_chain=(
    {
        "tags": itemgetter("tags"),
        "metadatas": itemgetter("metadatas"),
        "lang": itemgetter("lang"),
        "directories": itemgetter("directories"),
    }
    | _get_new_relations_and_tags_chain_prompt
    | llm4o
    | _parser
)