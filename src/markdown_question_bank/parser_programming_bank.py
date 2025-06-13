import os
from markdown_question_bank.question import MultilanguageString
from markdown_question_bank.programming_bank import ProgrammingBank, ProblemStatement

class ProgrammingBankParser:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def parse(self) -> ProgrammingBank:
        bank = ProgrammingBank()
        for subfolder in os.listdir(self.folder_path):
            subfolder_path = os.path.join(self.folder_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue
            translations = {}

            for filename in os.listdir(subfolder_path):
                if filename.endswith('.md'):
                    lang = filename.split('.')[0]
                    md_path = os.path.join(subfolder_path, filename)
                    with open(md_path, encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join([line for line in lines if not line.strip().startswith("<!--")]).strip()
                        translations[lang] = content
            if translations:
                statement = MultilanguageString(translations)
                problem = ProblemStatement(statement, title=subfolder)
                bank.add_problem(problem)
        return bank

if __name__ == "__main__":
    parser = ProgrammingBankParser("test_data/programming")
    programming_bank = parser.parse()
    for problem in programming_bank.get_problems():
        print(f"Title: {problem.get_title()}")
        for lang in problem.get_statement().get_languages():
            print(f"Statement ({lang}): {problem.get_statement().get_translation(lang)}")
        print()
