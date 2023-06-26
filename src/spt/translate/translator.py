import abc
import os
from typing import Iterable

import deepl

from ..exceptions import AuthorizationException


class ITranslator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate_text(self, text: Iterable[str]) -> list[str]:
        raise NotImplementedError()


class DeeplTranslator(ITranslator):
    def __init__(self) -> None:
        self.translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

    def translate_text(self, text: Iterable[str]) -> list[str]:
        try:
            return self.translator.translate_text(text, target_lang="JA")
        except deepl.exceptions.ConnectionException:
            err = ConnectionError()
            err.strerror = "ネットワークの接続を確認してください"
            raise err
        except deepl.exceptions.AuthorizationException:
            err = AuthorizationException()
            err.strerror = "DeepLの認証に失敗しました。APIキーが間違っている可能性があります。"
            raise err
