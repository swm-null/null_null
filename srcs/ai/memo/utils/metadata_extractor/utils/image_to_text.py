import asyncio
from openai import BaseModel
from pydantic import Field
from ai.utils.llm import llm4o
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser


class Image_description(BaseModel):
    image_description: str=Field("Description of image in user's language")
    ocr_text: str=""

async def image_to_text(image_urls: list[str], lang: str) -> list[Image_description]:
    extract_description_from_image_tasks=[asyncio.create_task(_extract_description_from_image(image, lang)) for image in image_urls]
    extracted_description_from_image: list[Image_description]=await asyncio.gather(*extract_description_from_image_tasks)
    
    return extracted_description_from_image

async def _extract_description_from_image(url: str, lang: str) -> Image_description:
    parser = JsonOutputParser(pydantic_object=Image_description)
    result = await llm4o.ainvoke(
        [
            HumanMessage(
                content=[
                    {
                        "type": "text", 
                        "text": f"Analyze this image and provide output in the following format and use {lang}:\n{parser.get_format_instructions()}"
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
