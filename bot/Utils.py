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

    @staticmethod
    def replace_bold(text: str) -> str:
        # Используем регулярное выражение для поиска и замены
        # \*\*(.*?)\*\* - ищет текст между двойными звездочками,
        # включая сами звездочки, и делает нежадный захват текста между ними
        # <b>\1</b> - заменяет найденный текст, где \1 ссылается на захваченный текст
        return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
