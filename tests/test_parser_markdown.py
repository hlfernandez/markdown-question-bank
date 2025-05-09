import os
from markdown_question_bank.parser_markown import MarkdownFolderParser

def test_parse_all_folder():
    folder_path = os.path.join("test_data", "all")

    parser = MarkdownFolderParser()

    questions = parser.parse(folder_path)

    assert len(questions) == 11, "There must be 11 questions in the folder"
    for q in questions:
        assert "GL" in q.get_languages()
        assert "ES" in q.get_languages()
        assert len(q.get_languages()) == 2, "There must be 2 language files in the folder"
        assert len(q.get_right_answers()) == 1
        assert len(q.get_wrong_answers()) == 2
        assert len(q.get_right_answers()) == 1
        assert len(q.get_wrong_answers()) == 2
    
    assert questions[0].get_right_answers()[0].get_translation("GL") == "Crea un iterador que produce os números 0, 1 e 2."
