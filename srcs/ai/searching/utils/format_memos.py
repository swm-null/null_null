from ai.searching._models.memo import Memo


def format_memos(memos: list[Memo]) -> str:
    return "\n".join(f"""
            ID: {memo.id}, {memo.timestamp}\n
            Metadata: {memo.metadata}\n\n
            Content: {memo.content}\n
        """ for memo in memos
    )
