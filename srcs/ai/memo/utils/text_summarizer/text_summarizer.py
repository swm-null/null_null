from ai.memo.utils.text_summarizer.chains import text_summarizer_chain


async def summarize_text(text: str, lang: str) -> str:
    return await text_summarizer_chain.ainvoke({"text": text, "lang": lang})