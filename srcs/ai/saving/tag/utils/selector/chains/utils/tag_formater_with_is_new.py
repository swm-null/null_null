from ai.saving._models.tag import Tag


def format_tags_with_is_new(tags: list[Tag]) -> str:
    return ", ".join(f"\"{tag.name}\" (new: {tag.is_new})" for tag in tags)
