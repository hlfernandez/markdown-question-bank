from markdown_question_bank.bank import Bank
from markdown_question_bank.question import Question

def test_bank_valid_questions():
    questions = [
        Question(
            statements={"GL": "Pregunta 1"},
            correct_answers={"GL": ["A"]},
            wrong_answers={"GL": ["B", "C"]},
            topics=["tema1"]
        ),
        Question(
            statements={"GL": "Pregunta 2"},
            correct_answers={"GL": ["Verdadeiro"]},
            wrong_answers={"GL": ["Falso", "Non sei"]},
            topics=["tema2"]
        )
    ]

    bank = Bank(questions=questions, min_wrong=2)

    assert len(bank.getQuestions()) == 2
    assert set(bank.getTopics()) == {"tema1", "tema2"}
    assert bank.getQuestionsByTopic("tema1")[0].getStatement("GL") == "Pregunta 1"
    assert "GL" in bank.getQuestions()[0].getLanguages()
