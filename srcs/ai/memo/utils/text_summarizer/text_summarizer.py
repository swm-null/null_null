from ai.memo.utils.text_summarizer.chains import text_summarizer, Text_summarizer_chain_output


async def summarize_text(text: str, lang: str) -> Text_summarizer_chain_output:
    return await text_summarizer(text, lang)
