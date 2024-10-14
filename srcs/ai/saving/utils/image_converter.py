import asyncio
from ai.utils.llm import llm4o
from langchain_core.messages import HumanMessage


async def convert_image_to_content(image_urls: list[str], lang: str) -> str:
    extract_description_from_image_tasks=[asyncio.to_thread(_extract_description_from_image, image, lang) for image in image_urls]
    extracted_description_from_image: list[str]=await asyncio.gather(*extract_description_from_image_tasks)
    
    return "image desciption:\n"+"\n".join(extracted_description_from_image)

def _extract_description_from_image(url: str, lang: str) -> str:
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
