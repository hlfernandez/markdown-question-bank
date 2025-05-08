import os
from typing import List
from markdown_question_bank.question import Question

class MarkdownFolderParser:
    def parse(self, folder: str, topics: List[str] = []) -> List[Question]:
        language_files = {
            f.split('.')[0].upper(): os.path.join(folder, f)
            for f in os.listdir(folder) if f.endswith('.md')
        }

        questions_by_lang: dict[str, List[tuple[str, List[str], List[str]]]] = {}

        for lang, path in language_files.items():
            with open(path, encoding="utf-8") as f:
                content = f.read()
            raw_questions = content.strip().split('---')
            parsed: List[tuple[str, List[str], List[str]]] = []
            for block in raw_questions:
                lines = block.strip().split('\n')
                if not lines:
                    continue
                statement = lines[0].strip()
                correct: List[str] = []
                wrong: List[str] = []
                for line in lines[1:]:
                    ans = line.strip()
                    if ans.endswith('`[X]`'):
                        ans_clean = ans[:-len('`[X]`')].strip()
                        correct.append(ans_clean)
                    elif ans:
                        wrong.append(ans)
                parsed.append((statement, correct, wrong))
            questions_by_lang[lang] = parsed

        question_count = len(next(iter(questions_by_lang.values())))
        for lang, questions in questions_by_lang.items():
            if len(questions) != question_count:
                raise ValueError(f"O número de preguntas en {lang} non coincide co resto.")

        questions: List[Question] = []
        for i in range(question_count):
            statements = {lang: questions_by_lang[lang][i][0] for lang in questions_by_lang}
            corrects = {lang: questions_by_lang[lang][i][1] for lang in questions_by_lang}
            if len(set(len(corrects[lang]) for lang in corrects)) != 1:
                raise ValueError(f"Na pregunta {statements} non hai o mesmo número de respostas correctas en todos os idiomas.")
            wrongs = {lang: questions_by_lang[lang][i][2] for lang in questions_by_lang}
            if len(set(len(wrongs[lang]) for lang in wrongs)) != 1:
                raise ValueError(f"Na pregunta {statements} non hai o mesmo número de respostas incorrectas en todos os idiomas.")
            
            questions.append(Question(statements, corrects, wrongs, topics))

        return questions


if __name__ == "__main__":
    # Exemplo de uso
    parser = MarkdownFolderParser()
    questions = parser.parse("test_data/all", topics=["topic1", "topic2"])
    for question in questions:
        print(question.getStatement("GL"))  # Cambia "EN" polo idioma que queiras
        print(question.getRightAnswers("GL"))
        print(question.getWrongAnswers("GL"))
        print(question.getTopics())