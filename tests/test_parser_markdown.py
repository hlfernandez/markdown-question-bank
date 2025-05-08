import os
from markdown_question_bank.parser_markown import MarkdownFolderParser

def test_parse_all_folder():
    folder_path = os.path.join("test_data", "all")

    parser = MarkdownFolderParser()

    questions = parser.parse(folder_path)

    assert len(questions) == 2, "There must be 2 questions in the folder"
    for q in questions:
        assert "GL" in q.getLanguages()
        assert "ES" in q.getLanguages()
        assert len(q.getLanguages()) == 2, "There must be 2 language files in the folder"
        assert len(q.getRightAnswers()) == 1
        assert len(q.getWrongAnswers()) == 2
        assert len(q.getRightAnswers()) == 1
        assert len(q.getWrongAnswers()) == 2
