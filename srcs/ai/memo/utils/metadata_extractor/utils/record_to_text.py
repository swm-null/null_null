import asyncio
import io
import requests
from ai.memo.utils.metadata_extractor.chains.record_summarizer_chain import record_summarizer, Record_summarizer_chain_output
from ai.utils.llm import openai_client
from fastapi.concurrency import run_in_threadpool


# available for mp3, mp4, mpeg, mpga, m4a, wav, webm, < 25mb
async def record_to_text(record_urls: list[str], lang: str) -> list[Record_summarizer_chain_output]:
    extract_description_from_record_tasks=[asyncio.create_task(_extract_description_from_record(record, lang)) for record in record_urls]
    extracted_description_from_record: list[Record_summarizer_chain_output]=await asyncio.gather(*extract_description_from_record_tasks)
    
    return extracted_description_from_record

async def _extract_description_from_record(url: str, lang: str) -> Record_summarizer_chain_output:
    record_file: bytes=await run_in_threadpool(_get_record_from_url, url)
    raw_transcript=await run_in_threadpool(_get_transcript_from_record, record_file, lang)
    result=await record_summarizer(raw_transcript, lang)

    return result

def _get_record_from_url(url: str) -> bytes:
    response=requests.get(url)
    record=io.BytesIO(response.content)
    
    return record.getvalue()

def _get_transcript_from_record(record_file: bytes, lang: str):
    return openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=("record.mp3", record_file),
        language="ko" if lang=="Korean" else "en",
    ).text
