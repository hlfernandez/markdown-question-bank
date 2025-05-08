import os
from markdown_question_bank.parser_markown import MarkdownFolderParser

def test_parse_all_folder():
    folder_path = os.path.join("test_data", "all")

    parser = MarkdownFolderParser()

    questions = parser.parse(folder_path)

    assert len(questions) == 2, "There must be 2 questions in the folder"
    for q in questions:
        assert "GL" in q.getLanguages()
        assert len(q.getLanguages()) == 2, "There must be 2 language files in the folder"
        assert q.getStatement("GL")
        assert len(q.getRightAnswers("GL")) == 1
        assert len(q.getWrongAnswers("GL")) == 2
        assert q.getStatement("ES")
        assert len(q.getRightAnswers("ES")) == 1
        assert len(q.getWrongAnswers("ES")) == 2
