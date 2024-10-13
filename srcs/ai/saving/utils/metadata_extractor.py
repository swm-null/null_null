from ai.saving.utils.chains.metadata_extractor_chain import metadata_extractor_chain


async def aextract_metadata(content: str, lang: str="Korean"):
    return metadata_extractor_chain.ainvoke({"content": content, "lang": lang})
    
def extract_metadata(content: str, lang: str="Korean") -> str:
    return metadata_extractor_chain.invoke({"content": content, "lang": lang})
