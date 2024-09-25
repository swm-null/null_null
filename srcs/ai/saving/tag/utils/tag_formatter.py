from ai.saving._models import Tag


def format_tags(tag_list: list[Tag]) -> str:
    return ", ".join(f"{tag.name} (id: {tag.id})" for tag in tag_list)
