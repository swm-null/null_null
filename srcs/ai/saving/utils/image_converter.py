import asyncio
from ai.saving.utils import image_to_text


async def convert_image_to_content(image_urls: list[str], lang: str) -> str:
    image_to_text_tasks=[asyncio.to_thread(image_to_text, image, lang) for image in image_urls]
    image_to_texts: list[str]=await asyncio.gather(*image_to_text_tasks)
    
    return "image desciption:\n"+"\n".join(image_to_texts)
