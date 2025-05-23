from typing import Dict, List

class MultilanguageString:
    def __init__(self, translations: Dict[str, str]):
        self.translations = translations

    def get_languages(self) -> List[str]:
        return list(self.translations.keys())

    def get_translation(self, language: str) -> str:
        return self.translations[language]

class Question:
    def __init__(
        self,
        statement: MultilanguageString,
        correct_answers: List[MultilanguageString],
        wrong_answers: List[MultilanguageString],
        topics: List[str],
        metadata: dict[str, dict[str, str]] | None = None
    ):
        self.statement = statement
        self.correct_answers = correct_answers
        self.wrong_answers = wrong_answers
        self.topics = topics
        self.metadata = metadata if metadata is not None else {}

    def get_languages(self) -> List[str]:
        return self.statement.get_languages()

    def get_statement(self) -> MultilanguageString:
        return self.statement

    def get_topics(self) -> List[str]:
        return self.topics

    def get_right_answers(self) -> List[MultilanguageString]:
        return self.correct_answers

    def get_wrong_answers(self) -> List[MultilanguageString]:
        return self.wrong_answers

    def get_metadata(self) -> Dict[str, Dict[str, str]]:
        return self.metadata
