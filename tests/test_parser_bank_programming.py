import os
from markdown_question_bank.parser_programming_bank import ProgrammingBankParser

def test_programming_bank_parser():
    parser = ProgrammingBankParser(os.path.join('test_data', 'programming'))
    bank = parser.parse()
    problems = bank.get_problems()
    assert len(problems) == 4, f"Expected 4 problems, got {len(problems)}"
    for problem in problems:
        langs = problem.get_statement().get_languages()
        assert set(langs) == {'EN', 'ES', 'GL'}, f"Expected languages EN, ES, GL, got {langs} for problem {problem.get_title()}"
