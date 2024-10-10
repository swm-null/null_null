from ai.saving.utils.chains.metadata_extractor_chain import Metadata_extractor_chain_output, metadata_extractor_chain


async def aextract_metadata(content: str, lang: str="Korean"):
    return metadata_extractor_chain.ainvoke({"content": content, "lang": lang})
    
def extract_metadata(content: str, lang: str="Korean") -> Metadata_extractor_chain_output:
    return metadata_extractor_chain.invoke({"content": content, "lang": lang})
