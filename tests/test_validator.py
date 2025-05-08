import pytest
from markdown_question_bank.validator import QuestionValidator
from markdown_question_bank.question import Question

def test_validate_all_detects_invalid_question():
    q1 = Question(
        statements={"GL": "Pregunta válida"},
        correct_answers={"GL": ["A"]},
        wrong_answers={"GL": ["B", "C"]},
        topics=[]
    )

    q2 = Question(
        statements={"GL": "Pregunta inválida"},
        correct_answers={"GL": ["A"]},
        wrong_answers={"GL": ["B"]},
        topics=[]
    )

    validator = QuestionValidator(min_wrong=2)

    with pytest.raises(ValueError, match="Erro na pregunta 2"):
        validator.validate_all([q1, q2])

def test_validate_all_valid_questions():
    q1 = Question(
        statements={"GL": "Pregunta 1"},
        correct_answers={"GL": ["A"]},
        wrong_answers={"GL": ["B", "C"]},
        topics=[]
    )

    q2 = Question(
        statements={"GL": "Pregunta 2"},
        correct_answers={"GL": ["Si"]},
        wrong_answers={"GL": ["Non", "Quizais"]},
        topics=[]
    )

    validator = QuestionValidator(min_wrong=2)
    validator.validate_all([q1, q2])