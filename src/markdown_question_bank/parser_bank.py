import os
from markdown_question_bank.bank import Bank
from markdown_question_bank.parser_markown import MarkdownFolderParser

class BankFolderParser:
    def __init__(self, min_wrong: int):
        self.min_wrong = min_wrong
        self.qparser = MarkdownFolderParser()

    def parse(self, root_folder: str) -> Bank:
        questions = []

        has_topic_dirs = any(
            os.path.isdir(os.path.join(root_folder, item))
            and not item.startswith(".")
            for item in os.listdir(root_folder)
        )

        if has_topic_dirs:
            for item in sorted(os.listdir(root_folder)):
                if item.startswith("."):
                    continue  # Skip hidden directories
                full_path = os.path.join(root_folder, item)
                if os.path.isdir(full_path):
                    topic = item
                    questions += self.qparser.parse(full_path, topics=[topic])
        else:
            questions = self.qparser.parse(root_folder, topics=[])

        return Bank(questions, min_wrong=self.min_wrong)

if __name__ == "__main__":
    folder_path = os.path.join("test_data", "bank")
    parser = BankFolderParser(min_wrong=2)
    bank = parser.parse(folder_path)

    questions = bank.get_questions()
    print(len(questions))

    print(questions[0].statement.get_translation("ES"))
    print(questions[0].get_right_answers()[0].get_translation("ES"))
    
    topics = bank.get_topics()
    print(topics)
