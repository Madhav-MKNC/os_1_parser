import re

from src.bookmapper import BookMapper
from src.langmapper import LanguageMapper


class MKNCUtils:
    def __init__(self):
        self.book_mapper = BookMapper()
        self.book_names = set(self.book_mapper.dictionary.values())
        self.lang_mapper = LanguageMapper()
        self.book_langs = set(self.lang_mapper.dictionary.values())

    def has_name(self, text: str) -> bool:
        return ' name ' in f" {text.lower()} " and '/o' in text.lower()

    def get_name(self, text: str) -> str:
        # Look for the pattern 'name' followed by the actual name and then the relation (e.g., 'S/O', 'W/O', etc.)
        match = re.search(r'\bname\s+([A-Za-z]+(?: [A-Za-z]+)*)\s+(?:S/O|W/O|D/O|B/O|P/O)\b', text, re.IGNORECASE)
        return match.group(1) if match else ""

    def has_book_name(self, text: str) -> bool:
        for b_n in self.book_names:
            if f" {b_n.lower()} " in f" {text.lower()} ":
                return True
        return False

    def get_book_name(self, text: str) -> str:
        for b_n in self.book_names:
            if f" {b_n.lower()} " in f" {text.lower()} ":
                return b_n
        return None

    def has_book_lang(self, text: str) -> bool:
        for b_l in self.book_langs:
            if f" {b_l.lower()} " in f" {text.lower()} ":
                return True
        return False

    def get_book_lang(self, text: str) -> str:
        for b_l in self.book_langs:
            if f" {b_l.lower()} " in f" {text.lower()} ":
                return b_l
        return None
