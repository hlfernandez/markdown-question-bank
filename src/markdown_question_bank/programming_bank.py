from typing import List
from markdown_question_bank.question import MultilanguageString

class ProblemStatement:
    def __init__(self, statement: MultilanguageString, title: str):
        self.statement = statement
        self.title = title

    def get_statement(self) -> MultilanguageString:
        return self.statement

    def get_title(self) -> str:
        return self.title

class ProgrammingBank:
    def __init__(self):
        self.problems: List[ProblemStatement] = []

    def add_problem(self, problem: ProblemStatement):
        self.problems.append(problem)

    def get_problems(self) -> List[ProblemStatement]:
        return self.problems
    
    def get_languages(self) -> list[str]:
        langs = set()
        for problem in self.problems:
            langs.update(problem.get_statement().get_languages())
        return sorted(langs)
