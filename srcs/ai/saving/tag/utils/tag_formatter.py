from ai.saving._models import Tag


def format_tags(tags: list[Tag]) -> str:
    return ", ".join(f"\"{tag.name}\"" for tag in tags)
