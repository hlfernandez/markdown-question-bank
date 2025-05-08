import pytest

from markdown_question_bank.bank import Bank
from markdown_question_bank.question import Question, MultilanguageString

def test_bank_valid_questions():
    questions = [
        Question(
            statement=MultilanguageString({"GL": "Pregunta 1"}),
            correct_answers=[MultilanguageString({"GL": "A"})],
            wrong_answers=[
                MultilanguageString({"GL": "B"}),
                MultilanguageString({"GL": "C"})
            ],
            topics=["tema1"]
        ),
        Question(
            statement=MultilanguageString({"GL": "Pregunta 2"}),
            correct_answers=[MultilanguageString({"GL": "Verdadeiro"})],
            wrong_answers=[
                MultilanguageString({"GL": "Falso"}),
                MultilanguageString({"GL": "Non sei"})
            ],
            topics=["tema2"]
        )
    ]

    bank = Bank(questions=questions, min_wrong=2)

    assert len(bank.get_questions()) == 2
    assert set(bank.get_topics()) == {"tema1", "tema2"}
    assert bank.get_questions_by_topic("tema1")[0].get_statement().get_translation("GL") == "Pregunta 1"
    assert "GL" in bank.get_questions()[0].get_languages()

def test_bank_invalid_questions():
    questions = [
        Question(
            statement=MultilanguageString({"GL": "Pregunta 1", "ES": "Pregunta 1"}),
            correct_answers=[MultilanguageString({"GL": "A", "ES": "A"})],
            wrong_answers=[
                MultilanguageString({"GL": "B", "ES": "B"}),
                MultilanguageString({"GL": "C", "ES": "C"})
            ],
            topics=["tema1"]
        ),
        Question(
            statement=MultilanguageString({"GL": "Pregunta 2"}),
            correct_answers=[MultilanguageString({"GL": "Verdadeiro"})],
            wrong_answers=[
                MultilanguageString({"GL": "Falso"}),
                MultilanguageString({"GL": "Non sei"})
            ],
            topics=["tema2"]
        )
    ]

    with pytest.raises(ValueError, match="As preguntas non teñen os mesmos idiomas."):
        Bank(questions=questions, min_wrong=2)

