import os
from typing import List
from markdown_question_bank.question import Question, MultilanguageString

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

                # Extract the statement (can span multiple lines until the first answer starts)
                statement_lines = []
                answer_lines = []
                is_answer_section = False

                for line in lines:
                    # Detect the start of an answer (correct or not) only if the dash is at the beginning (ignoring whitespace)
                    if line.lstrip().startswith('- [X]') or (line.lstrip().startswith('-') and not line.lstrip().startswith('- [X]')):
                        is_answer_section = True
                    if is_answer_section:
                        answer_lines.append(line)
                    else:
                        statement_lines.append(line)

                statement = '\n'.join(statement_lines).strip()

                # Process answers (can span multiple lines)
                correct: List[str] = []
                wrong: List[str] = []
                current_answer = []
                is_correct = False

                for line in answer_lines:
                    if line.lstrip().startswith('- [X]'):
                        if current_answer:
                            answer_text = '\n'.join(current_answer).strip()
                            if is_correct:
                                correct.append(answer_text)
                            else:
                                wrong.append(answer_text)
                        current_answer = [line.lstrip()[5:].strip()]
                        is_correct = True
                    elif line.lstrip().startswith('-') and not line.lstrip().startswith('- [X]'):
                        if current_answer:
                            answer_text = '\n'.join(current_answer).strip()
                            if is_correct:
                                correct.append(answer_text)
                            else:
                                wrong.append(answer_text)
                        current_answer = [line.lstrip()[1:].strip()]
                        is_correct = False
                    else:
                        current_answer.append(line)

                # Add the last answer
                if current_answer:
                    answer_text = '\n'.join(current_answer).strip()
                    if is_correct:
                        correct.append(answer_text)
                    else:
                        wrong.append(answer_text)

                parsed.append((statement, correct, wrong))
            questions_by_lang[lang] = parsed

        question_count = len(next(iter(questions_by_lang.values())))
        for lang, questions in questions_by_lang.items():
            if len(questions) != question_count:
                raise ValueError(f"O número de preguntas en {lang} non coincide co resto.")

        toret: List[Question] = []
        for i in range(question_count):
            statements = {lang: questions_by_lang[lang][i][0] for lang in questions_by_lang}
            corrects = {lang: questions_by_lang[lang][i][1] for lang in questions_by_lang}
            if len(set(len(corrects[lang]) for lang in corrects)) != 1:
                raise ValueError(f"Na pregunta {statements} non hai o mesmo número de respostas correctas en todos os idiomas.")
            wrongs = {lang: questions_by_lang[lang][i][2] for lang in questions_by_lang}
            if len(set(len(wrongs[lang]) for lang in wrongs)) != 1:
                raise ValueError(f"Na pregunta {statements} non hai o mesmo número de respostas incorrectas en todos os idiomas.")

            statement_ml = MultilanguageString(statements)
            correct_answers_ml = [MultilanguageString({lang: corrects[lang][j] for lang in corrects}) for j in range(len(next(iter(corrects.values()))))]
            wrong_answers_ml = [MultilanguageString({lang: wrongs[lang][j] for lang in wrongs}) for j in range(len(next(iter(wrongs.values()))))]

            toret.append(Question(statement_ml, correct_answers_ml, wrong_answers_ml, topics))

        return toret


if __name__ == "__main__":
    parser = MarkdownFolderParser()
    test_questions = parser.parse("test_data/all", topics=["topic1", "topic2"])
    for question in test_questions:
        print('*' * 20)
        print(question.get_statement().get_translation("GL"))
        print(len(question.get_right_answers()))
        print(len(question.get_wrong_answers()))
        print(question.get_right_answers()[0].get_translation("GL"))
        for q in question.get_wrong_answers():
            print('- ' + q.get_translation("GL"))
        print(question.get_topics())