from ai.memo.structure.processor.utils.locate_memos.utils.locate_tags.utils.get_structure_dict import get_structure_dict
from ai.memo.structure.processor.utils.locate_memos.utils.get_tag_dict import get_tag_dict


async def get_current_structure(user_id: str) -> dict[str, list[str]]:
    tag_id_to_name, tag_name_to_id=await get_tag_dict(user_id)
    
    return await get_structure_dict(user_id, tag_id_to_name, tag_name_to_id)
