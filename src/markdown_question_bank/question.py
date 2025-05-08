from typing import Dict, List

class Question:
    def __init__(
        self,
        statements: Dict[str, str],
        correct_answers: Dict[str, List[str]],
        wrong_answers: Dict[str, List[str]],
        topics: List[str]
    ):
        self.statements = statements
        self.correct_answers = correct_answers
        self.wrong_answers = wrong_answers
        self.topics = topics

    def getLanguages(self) -> List[str]:
        return list(self.statements.keys())

    def getStatement(self, language: str) -> str:
        return self.statements[language]

    def getTopics(self) -> List[str]:
        return self.topics

    def getRightAnswers(self, language: str) -> List[str]:
        return self.correct_answers[language]

    def getWrongAnswers(self, language: str) -> List[str]:
        return self.wrong_answers[language]
