import os
from typing import List
from markdown_question_bank.quiz_model import QuizModel
from markdown_question_bank.quiz_markdown import MarkdownQuizModel

class QuizExporter:
    def __init__(self, outdir: str, num_cols: int):
        self.outdir = outdir
        self.num_cols = num_cols

    def export_models(self, models: List[QuizModel], languages: List[str]) -> List[str]:
        os.makedirs(self.outdir, exist_ok=True)
        generated_files = []

        for i, model in enumerate(models):
            markdown_quiz = MarkdownQuizModel(model)
            for lang in languages:
                base_path = os.path.join(self.outdir, f"{i}_{lang}.md")
                with_answers_path = os.path.join(self.outdir, f"{i}_{lang}_with_answers.md")

                markdown_quiz.to_file(base_path, lang, num_cols=self.num_cols, with_true_answers=False)
                markdown_quiz.to_file(with_answers_path, lang, num_cols=self.num_cols, with_true_answers=True)

                generated_files.extend([base_path, with_answers_path])

        return generated_files
