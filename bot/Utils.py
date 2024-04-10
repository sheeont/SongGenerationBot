import re


class Utils:
    @staticmethod
    def contains_english_chars(text: str) -> bool:
        pattern = r'[a-zA-Z]'
        return bool(re.search(pattern, text))

    @staticmethod
    def replace_english_chars(text: str, repl_text: str) -> str:
        pattern = r'[a-zA-Z]+'
        return re.sub(pattern, repl_text, text)
