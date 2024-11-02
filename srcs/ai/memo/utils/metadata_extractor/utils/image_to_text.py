import asyncio
import json
from openai import BaseModel
from ai.utils.llm import llm4o
from langchain_core.messages import HumanMessage
import textwrap


class Image_description(BaseModel):
    image_description: str
    ocr_text: str

async def image_to_text(image_urls: list[str], lang: str) -> list[Image_description]:
    extract_description_from_image_tasks=[asyncio.create_task(_extract_description_from_image(image, lang)) for image in image_urls]
    extracted_description_from_image: list[Image_description]=await asyncio.gather(*extract_description_from_image_tasks)
    
    return extracted_description_from_image

async def _extract_description_from_image(url: str, lang: str) -> Image_description:
    result=await llm4o.ainvoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": textwrap.dedent(f"""
                        Please provide the following response in **JSON** format:
                        {{
                        "image_description": "<image summary in {lang}>",
                        "ocr_text": "<OCR text if any>"
                        }}
                    """)},
                    {"type": "image_url", "image_url": {"url": url}}
                ]
            )
        ]
    )
    raw_content = result.content[8:-4]

    return Image_description.model_validate_json(raw_content)
