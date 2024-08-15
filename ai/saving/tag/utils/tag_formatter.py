from ai.saving.tag._models.tag import Tag


def tag_formatter(tag_list: list[Tag]) -> str:
    return ", ".join(f"{tag.name} (id: {tag.id})" for tag in tag_list)
