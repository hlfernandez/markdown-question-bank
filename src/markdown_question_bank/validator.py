from typing import List

from markdown_question_bank.question import Question


class QuestionValidator:
    def __init__(self, min_wrong: int):
        self.min_wrong = min_wrong

    def validate(self, question: Question) -> None:
        for lang in question.getLanguages():
            if not question.getRightAnswers(lang):
                raise ValueError(f"A pregunta non ten respostas correctas en {lang}.")
            if len(question.getWrongAnswers(lang)) < self.min_wrong:
                raise ValueError(
                    f"A pregunta ten menos de {self.min_wrong} respostas incorrectas en {lang}."
                )

    def validate_all(self, questions: List[Question]) -> None:
        for i, q in enumerate(questions):
            try:
                self.validate(q)
            except ValueError as e:
                raise ValueError(f"Erro na pregunta {i + 1}: {e}") from e
