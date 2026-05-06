import os
from markdown_question_bank.question import MultilanguageString
from markdown_question_bank.programming_bank import ProgrammingBank, ProblemStatement

class ProgrammingBankParser:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def _parse_problem_dir(self, dir_path: str, title: str) -> ProblemStatement | None:
        translations = {}
        for filename in os.listdir(dir_path):
            if filename.endswith('.md'):
                lang = filename.split('.')[0]
                md_path = os.path.join(dir_path, filename)
                with open(md_path, encoding="utf-8") as f:
                    lines = f.readlines()
                    content = "".join([line for line in lines if not line.strip().startswith("<!--")]).strip()
                    translations[lang] = content
        if translations:
            return ProblemStatement(MultilanguageString(translations), title=title)
        return None

    def parse(self) -> ProgrammingBank:
        bank = ProgrammingBank()
        for entry in os.listdir(self.folder_path):
            entry_path = os.path.join(self.folder_path, entry)
            if not os.path.isdir(entry_path):
                continue

            # Check if this directory contains .md files directly
            has_md_files = any(f.endswith('.md') for f in os.listdir(entry_path))
            if has_md_files:
                problem = self._parse_problem_dir(entry_path, title=entry)
                if problem:
                    bank.add_problem(problem)
            else:
                # Recurse one level deeper, using "parent/child" as the title
                for subentry in os.listdir(entry_path):
                    subentry_path = os.path.join(entry_path, subentry)
                    if not os.path.isdir(subentry_path):
                        continue
                    problem = self._parse_problem_dir(subentry_path, title=f"{entry}/{subentry}")
                    if problem:
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
