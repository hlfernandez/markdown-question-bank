import os
from markdown_question_bank.parser_markown import MarkdownFolderParser

def test_parse_mini_folder():
    folder_path = os.path.join("test_data", "mini")

    parser = MarkdownFolderParser()

    questions = parser.parse(folder_path)
    assert len(questions) == 3, "There must be 3 questions in the test_data/mini folder"


def test_parse_all_folder():
    folder_path = os.path.join("test_data", "all")

    parser = MarkdownFolderParser()

    questions = parser.parse(folder_path)

    assert len(questions) == 12, "There must be 12 questions in the folder"
    for q in questions:
        assert len(q.get_languages()) == 3, "There must be 3 language files in the test_data/all folder"

        assert "EN" in q.get_languages()
        assert "GL" in q.get_languages()
        assert "ES" in q.get_languages()

        assert len(q.get_right_answers()) == 1
        assert len(q.get_wrong_answers()) == 2

        statement_gl = q.get_statement().get_translation("GL")
        if "[este anexo]" in statement_gl:
            appendix = q.get_appendix()
            assert appendix is not None, "Question with appendix reference must have appendix object"
            assert appendix.get_content().get_translation("GL").startswith("```python\ndef misterio"), "Appendix content must match code block"

            assert appendix.get_title("GL") == "Código 1", "Appendix title must match the expected value"
            assert appendix.get_url("GL") == "#código-1", "Appendix URL must match the expected value"
            
            assert appendix.get_title("ES") == "Código 1", "Appendix title must match the expected value"
            assert appendix.get_url("ES") == "#código-1", "Appendix URL must match the expected value"

            assert appendix.get_title("EN") == "Code 1", "Appendix title must match the expected value"
            assert appendix.get_url("EN") == "#code-1", "Appendix URL must match the expected value"
    
    assert questions[0].get_right_answers()[0].get_translation("GL") == "Crea un iterador que produce os números 0, 1 e 2."
    assert questions[11].get_statement().get_translation("GL") == "Considerando a asignación inicial da variable A na primeira liña, indica o caso en que se modifica o valor que se mostraría para a variable A despois de executar as outras dúas instrucións:"

    assert len(questions[0].get_metadata()['ES']) == 0, "Metadata for question 0 must be empty"
    assert len(questions[11].get_metadata()['ES']) == 2, "Metadata for question 11 must contain two languages"

