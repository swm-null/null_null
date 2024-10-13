from ai.utils.llm import llm4o
from langchain_core.messages import HumanMessage


def image_to_text(url: str, lang: str) -> str:
    result=llm4o.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": f"Summarize the image for me. If there is text, please add the OCR of the original text to the image description. Summarize it in {lang}."},
                    {"type": "image_url", "image_url": {"url": url}}
                ]
            )
        ]
    )
    
    return str(result.content)
