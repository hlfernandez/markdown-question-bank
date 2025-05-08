import os
from markdown_question_bank.parser_bank import BankFolderParser

def test_parse_bank_with_topics():
    folder_path = os.path.join("test_data", "bank")
    parser = BankFolderParser(min_wrong=2)
    bank = parser.parse(folder_path)

    questions = bank.getQuestions()
    assert len(questions) >= 1, "Debe haber polo menos unha pregunta no banco"
    
    topics = bank.getTopics()
    assert "topic1" in topics
    assert "topic2" in topics or len(topics) == 1  # Por se topic2 aínda non ten preguntas

    for q in questions:
        assert q.getTopics(), "Cada pregunta debe ter polo menos un tema"
        assert bank.min_wrong <= len(q.getWrongAnswers())
