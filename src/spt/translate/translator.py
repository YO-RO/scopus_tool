import abc
import os
from typing import Iterable

import deepl


class ITranslator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate_text(self, text: Iterable[str]) -> list[str]:
        raise NotImplementedError()


class DeeplTranslator(ITranslator):
    def __init__(self) -> None:
        self.translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

    def translate_text(self, text: Iterable[str]) -> list[str]:
        return self.translator.translate_text(text, target_lang="JA")
