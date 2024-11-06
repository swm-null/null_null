from ai.memo._models import Tag


def get_tag_name_to_id(tags: list[Tag]) -> dict[str, str]:
    result={}
    for tag in tags:
        result[tag.name]=tag.id
    
    return result
