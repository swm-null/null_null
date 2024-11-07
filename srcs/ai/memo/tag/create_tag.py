import asyncio
import logging
import uuid
from ai.memo.tag.utils import determine_tag_names_chain, Determine_tag_names_chain_output
from ai.memo.utils import get_tag_name_to_id, get_tags_from_db, get_current_structure
from routers._models.memo import Memo_raw_memo, Memo_tag_name_and_id
from ai.memo.utils import process_metadata
from fastapi.concurrency import run_in_threadpool
from fastapi.concurrency import run_in_threadpool


async def create_tag(user_id: str, raw_memo: Memo_raw_memo, lang: str="Korean") -> list[Memo_tag_name_and_id]:    
    logging.info("create_tag] \nuser_id: %s, \nraw_memo: %s", user_id, raw_memo)
    content, existing_tags, current_structure=await asyncio.gather(
        process_metadata(raw_memo.content, raw_memo.image_urls, raw_memo.voice_urls, lang),
        run_in_threadpool(get_tags_from_db, user_id),
        get_current_structure(user_id)
    )
    
    selected_tag_names_by_chain: list[str]=await _determine_tag_names(content, current_structure, lang)
    tag_name_to_id: dict[str, str]=get_tag_name_to_id(existing_tags)
    assigned_tags: list[Memo_tag_name_and_id]=_assign_tag_id(selected_tag_names_by_chain, tag_name_to_id)
    
    return assigned_tags

async def _determine_tag_names(content: str, current_structure: dict[str, list[str]], lang: str) -> list[str]:
    determined_tag_names: Determine_tag_names_chain_output=await determine_tag_names_chain(content, current_structure, lang)
    
    return determined_tag_names.selected_tag_names + determined_tag_names.new_tag_names

def _assign_tag_id(selected_tag_names_by_chain: list[str], tag_name_to_id: dict[str, str]) -> list[Memo_tag_name_and_id]:
    return [
        Memo_tag_name_and_id(
            id=uuid.uuid4().hex if selected_tag_name not in tag_name_to_id else tag_name_to_id[selected_tag_name],
            name=selected_tag_name,
            is_new=selected_tag_name in tag_name_to_id
        ) for selected_tag_name in selected_tag_names_by_chain
    ]
