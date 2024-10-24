from ai.memo._models import Tag


def is_new_tag(tag: Tag) -> bool:
    return tag.id==tag.name
