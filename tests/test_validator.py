import pytest
from markdown_question_bank.validator import QuestionValidator
from markdown_question_bank.question import Question, MultilanguageString

def test_validate_all_detects_invalid_question():
    q1 = Question(
        statement=MultilanguageString({"GL": "Pregunta válida"}),
        correct_answers=[MultilanguageString({"GL": "A"})],
        wrong_answers=[MultilanguageString({"GL": "B"}), MultilanguageString({"GL": "C"})],
        topics=[]
    )

    q2 = Question(
        statement=MultilanguageString({"GL": "Pregunta inválida"}),
        correct_answers=[MultilanguageString({"GL": "A"})],
        wrong_answers=[MultilanguageString({"GL": "B"})],
        topics=[]
    )

    validator = QuestionValidator(min_wrong=2)

    with pytest.raises(ValueError, match="Erro na pregunta 2"):
        validator.validate_all([q1, q2])

def test_validate_all_valid_questions():
    q1 = Question(
        statement=MultilanguageString({"GL": "Pregunta 1"}),
        correct_answers=[MultilanguageString({"GL": "A"})],
        wrong_answers=[MultilanguageString({"GL": "B"}), MultilanguageString({"GL": "C"})],
        topics=[]
    )

    q2 = Question(
        statement=MultilanguageString({"GL": "Pregunta 2"}),
        correct_answers=[MultilanguageString({"GL": "Si"})],
        wrong_answers=[MultilanguageString({"GL": "Non"}), MultilanguageString({"GL": "Quizais"})],
        topics=[]
    )

    validator = QuestionValidator(min_wrong=2)
    validator.validate_all([q1, q2])