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

    assert len(bank.getQuestions()) == 2
    assert set(bank.getTopics()) == {"tema1", "tema2"}
    assert bank.getQuestionsByTopic("tema1")[0].getStatement().getTranslation("GL") == "Pregunta 1"
    assert "GL" in bank.getQuestions()[0].getLanguages()
