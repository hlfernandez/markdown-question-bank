from typing import Dict, List

class MultilanguageString:
    def __init__(self, translations: Dict[str, str]):
        self.translations = translations

    def getLanguages(self) -> List[str]:
        return list(self.translations.keys())

    def getTranslation(self, language: str) -> str:
        return self.translations[language]

class Question:
    def __init__(
        self,
        statement: MultilanguageString,
        correct_answers: List[MultilanguageString],
        wrong_answers: List[MultilanguageString],
        topics: List[str]
    ):
        self.statement = statement
        self.correct_answers = correct_answers
        self.wrong_answers = wrong_answers
        self.topics = topics

    def getLanguages(self) -> List[str]:
        return self.statement.getLanguages()

    def getStatement(self) -> MultilanguageString:
        return self.statement

    def getTopics(self) -> List[str]:
        return self.topics

    def getRightAnswers(self) -> List[MultilanguageString]:
        return self.correct_answers

    def getWrongAnswers(self) -> List[MultilanguageString]:
        return self.wrong_answers
