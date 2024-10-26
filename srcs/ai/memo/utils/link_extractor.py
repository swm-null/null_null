import re


url_regex=r"(https?://[^\s]+|www\.[^\s]+|\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\b)"

def extract_link(text: str) -> list[str]:
    return re.findall(url_regex, text)
