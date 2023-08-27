import sys
import os

import config
from importlib import import_module


class Language():
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        languages_directory = os.path.abspath(os.path.join(current_directory, '../languages'))
        sys.path.insert(0, languages_directory)
    def get_languages(self) -> tuple:
        languages = {lib[:-3] if lib.endswith(".py") else config.default_language for lib in os.listdir(f"{config.directory}languages")}
        return tuple(languages)

    def get_text(self, key: str, language: str = None) -> str:
        language = language if language else config.default_language
        text = getattr(import_module(language), key, None)
        return text
