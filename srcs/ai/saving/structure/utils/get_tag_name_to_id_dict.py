from ai.saving.structure.utils.directory_format import _get_tags_from_db


def get_tag_name_to_id_dict(user_id: str) -> dict[str, str]:
    tag_id_to_name, tag_name_to_id=_get_tags_from_db(user_id)
    
    return tag_name_to_id
    
