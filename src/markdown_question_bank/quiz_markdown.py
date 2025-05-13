import math
from typing import List
from markdown_question_bank.quiz_model import QuizModel

class MarkdownQuizModel:
    def __init__(self, quiz_model: QuizModel):
        self.quiz_model = quiz_model

    def get_languages(self) -> List[str]:
        if not self.quiz_model.questions:
            return []
        return self.quiz_model.questions[0].statement.get_languages()

    def _render_answer_tables(self, num_cols: int, with_true_answers: bool) -> List[str]:
        lines = []
        questions = self.quiz_model.get_questions()
        total = len(questions)
        num_blocks = math.ceil(total / num_cols)

        for block in range(num_blocks):
            start = block * num_cols
            end = min(start + num_cols, total)
            block_questions = questions[start:end]

            # Header and separator
            header = ["   "] + [f"P{start + i + 1}" for i in range(len(block_questions))]
            separator = ["---" for _ in header]
            lines.append("| " + " | ".join(header) + " |")
            lines.append("| " + " | ".join(separator) + " |")

            num_options = max(len(q.options) for q in block_questions)
            for row in range(num_options):
                label = f"{chr(65 + row)}"  # A, B, C, ...
                line = [label]
                for q in block_questions:
                    if row < len(q.options):
                        if with_true_answers and row in q.correct_indices:
                            line.append("X")
                        else:
                            line.append(" ")
                    else:
                        line.append(" ")
                lines.append("| " + " | ".join(line) + " |")

            lines.append("")

        return lines

    def render_markdown(self, language: str, num_cols: int = 4, with_true_answers: bool = False) -> str:
        lines = []

        # Táboas de respostas en bloques
        lines.extend(self._render_answer_tables(num_cols, with_true_answers))

        # Construír preguntas
        for i, question in enumerate(self.quiz_model.get_questions(), 1):
            lines.append(f"**Pregunta {i}**. {question.statement.get_translation(language)}")
            lines.append("")
            for idx, option in enumerate(question.options):
                prefix = "- [X] " if with_true_answers and idx in question.correct_indices else "- "
                lines.append(f"{prefix}{option.get_translation(language)}")
            lines.append("")

        return "\n".join(lines)

    def to_file(self, output_path: str, language: str, num_cols: int = 4, with_true_answers: bool = False):
        """
        Writes the rendered markdown to a file.

        :param output_path: Path to the output file.
        :param language: Language for the markdown content.
        :param num_cols: Number of columns for the answer tables.
        :param with_true_answers: Whether to include true answers in the output.
        """
        markdown_content = self.render_markdown(language, num_cols, with_true_answers)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
