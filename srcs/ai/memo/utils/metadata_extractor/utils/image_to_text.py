import asyncio
from openai import BaseModel
from pydantic import Field
from ai.utils.llm import llm4o_mini
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from ai.utils import retry_on_timeout


class Image_description(BaseModel):
    simple_description: str=Field(description="Simple text to be provided with a preview. So that users know what this image is about. Words rather than sentences.")
    image_description: str=Field(description="Description of image in user's language")
    ocr_text: str=""

async def image_to_text(image_urls: list[str], lang: str) -> list[Image_description]:
    extract_description_from_image_tasks=[retry_on_timeout(lambda: _extract_description_from_image(image, lang), retry_count=3, timeout=30) for image in image_urls]
    extracted_description_from_image: list[Image_description]=await asyncio.gather(*extract_description_from_image_tasks)
    
    return extracted_description_from_image

async def _extract_description_from_image(url: str, lang: str) -> Image_description:
    parser = JsonOutputParser(pydantic_object=Image_description)
    result = await llm4o_mini.ainvoke(
        [
            HumanMessage(
                content=[
                    {
                        "type": "text", 
                        "text": f"Analyze thi s image and provide output in the following format and use {lang}:\n{parser.get_format_instructions()}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": url}
                    }
                ]
            )
        ]
    )
    parsed_response = parser.parse(result.content) # type: ignore
    
    return parsed_response
