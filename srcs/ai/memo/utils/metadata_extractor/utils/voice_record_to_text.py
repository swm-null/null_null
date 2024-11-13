import asyncio
import io
import os
from urllib import parse
import requests
from ai.memo.utils.metadata_extractor.chains.voice_record_summarizer_chain import voice_record_summarizer, Voice_record_summarizer_chain_output
from ai.utils.llm import openai_client
from fastapi.concurrency import run_in_threadpool


# available for mp3, mp4, mpeg, mpga, m4a, wav, webm, < 25mb
async def voice_record_to_text(voice_record_urls: list[str], lang: str) -> list[Voice_record_summarizer_chain_output]:
    extract_description_from_voice_record_tasks=[asyncio.create_task(_extract_description_from_voice_record(voice_record, lang)) for voice_record in voice_record_urls]
    extracted_description_from_voice_record: list[Voice_record_summarizer_chain_output]=await asyncio.gather(*extract_description_from_voice_record_tasks)
    
    return extracted_description_from_voice_record

async def _extract_description_from_voice_record(url: str, lang: str) -> Voice_record_summarizer_chain_output:
    voice_record_file: bytes=await run_in_threadpool(_get_voice_record_from_url, url)
    file_extension: str=_get_file_extension_from_url(url)
    print(f"record{file_extension}")
    raw_transcript=await run_in_threadpool(_get_transcript_from_voice_record, voice_record_file, file_extension, lang)
    result=await voice_record_summarizer(raw_transcript, lang)

    return result

def _get_voice_record_from_url(url: str) -> bytes:
    response=requests.get(url)
    voice_record=io.BytesIO(response.content)
    
    return voice_record.getvalue()

def _get_file_extension_from_url(url: str) -> str:
    parsed_url=parse.urlparse(url)
    _, ext=os.path.splitext(parsed_url.path)
    
    return ext
    
def _get_transcript_from_voice_record(voice_record_file: bytes, file_extension: str, lang: str):
    return openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=(f"record{file_extension}", voice_record_file),
        language="ko" if lang=="Korean" else "en",
    ).text
