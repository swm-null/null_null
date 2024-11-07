from operator import itemgetter
import textwrap
from langchain_core.output_parsers import StrOutputParser
from ai.utils.llm import llm4o_mini
from langchain_core.prompts import PromptTemplate


_parser = StrOutputParser()

_text_summarizer_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    The text you receive is the content crawled from a site.
    You need to summarize the text you receive.

    The summary should contain information about what this website contains, and should contain a description of the given text. I think the length of the description should be about a half of the length of the given text.

    Summarize it in detail so that you can find the information you want from the content of this site by just looking at this summary later. However, unnecessary information does not have to be included in the summary.

    Do not do any work such as adding headings or structuring the output, but output it as a simple line of text.
    And summarize it in the language that the user uses.

    User's language: {lang}

    {text}
    """)
)

text_summarizer_chain=(
    {
        "text": itemgetter("text"),
        "lang": itemgetter("lang"),
    }
    | _text_summarizer_chain_prompt
    | llm4o_mini
    | _parser
)
