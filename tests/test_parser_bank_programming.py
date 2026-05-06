import os
from markdown_question_bank.parser_programming_bank import ProgrammingBankParser

def test_programming_bank_parser():
    parser = ProgrammingBankParser(os.path.join('test_data', 'programming'))
    bank = parser.parse()
    problems = bank.get_problems()
    assert len(problems) == 6, f"Expected 6 problems, got {len(problems)}"
    for problem in problems:
        langs = problem.get_statement().get_languages()
        assert set(langs) == {'EN', 'ES', 'GL'}, f"Expected languages EN, ES, GL, got {langs} for problem {problem.get_title()}"

def test_programming_bank_parser_nested_dirs():
    parser = ProgrammingBankParser(os.path.join('test_data', 'programming'))
    bank = parser.parse()
    titles = {p.get_title() for p in bank.get_problems()}
    assert 'lists/1' in titles, f"Expected 'lists/1' in titles, got {titles}"
    assert 'lists/2' in titles, f"Expected 'lists/2' in titles, got {titles}"
