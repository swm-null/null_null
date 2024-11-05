from ai.memo.utils import get_structure_dict, get_tag_dict


async def get_current_structure(user_id: str) -> dict[str, list[str]]:
    tag_id_to_name, tag_name_to_id=await get_tag_dict(user_id)
    
    return await get_structure_dict(user_id, tag_id_to_name, tag_name_to_id)
