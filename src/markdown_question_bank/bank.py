from typing import List
from markdown_question_bank.question import Question
from markdown_question_bank.validator import QuestionValidator

class Bank:
    def __init__(self, questions: List[Question], min_wrong: int):
        self.questions = questions
        self.min_wrong = min_wrong
        self._validate_questions()
        self.languages = self._check_languages()

    def _validate_questions(self):
        validator = QuestionValidator(self.min_wrong)
        validator.validate_all(self.questions)

    def _check_languages(self) -> List[str]:
        if not self.questions:
            return []
        base = set(self.questions[0].get_languages())
        for q in self.questions[1:]:
            if set(q.get_languages()) != base:
                raise ValueError("As preguntas non teñen os mesmos idiomas.")

        return list(base)

    def get_questions(self) -> List[Question]:
        return self.questions

    def get_topics(self) -> List[str]:
        topics = set()
        for q in self.questions:
            topics.update(q.get_topics())

        return list(topics)

    def get_questions_by_topic(self, topic: str) -> List[Question]:
        return [q for q in self.questions if topic in q.get_topics()]

    def filter_topics(self, excluded_topics: List[str]) -> 'Bank':
        filtered_questions = [
            q for q in self.questions
            if not any(topic in excluded_topics for topic in q.get_topics())
        ]

        return Bank(filtered_questions, self.min_wrong)
