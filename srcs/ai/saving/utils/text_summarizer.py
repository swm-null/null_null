from ai.utils.llm import llm4o
from .chains.text_summarizer_chain import text_summarizer_chain

def summarize_text(text: str, lang: str) -> str:
    return text_summarizer_chain.invoke({"text": text, "lang": lang})
