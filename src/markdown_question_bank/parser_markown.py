import os
from typing import List
from markdown_question_bank.question import Question, MultilanguageString, Appendix
import re

class MarkdownFolderParser:
    def parse(self, folder: str, topics: list[str] | None = None) -> List[Question]:
        if topics is None:
            topics = []
        language_files = {
            filename.split('.')[0].upper(): os.path.join(folder, filename)
            for filename in os.listdir(folder) if filename.endswith('.md')
        }

        # --- Parse appendices for each language ---
        appendices_by_lang: dict[str, dict[str, tuple[str, str]]] = {}
        for lang, path in language_files.items():
            with open(path, encoding="utf-8") as f:
                content = f.read()
            # Find appendix section
            appendix_section = re.search(r"^#\s*Anexos(.+)$", content, re.DOTALL | re.MULTILINE)
            appendices = {}
            if appendix_section:
                appendix_text = appendix_section.group(1)
                # Split by appendix headings (## ...), keep heading in result
                appendix_blocks = re.split(r'(^##\s+.+$)', appendix_text, flags=re.MULTILINE)
                # The split will result in ['', '## Title1', '...content1...', '## Title2', '...content2...', ...]
                for i in range(1, len(appendix_blocks), 2):
                    heading = appendix_blocks[i].strip()
                    content_block = appendix_blocks[i+1] if (i+1) < len(appendix_blocks) else ''
                    title = heading[2:].strip()
                    code = content_block.strip('\n')
                    url = f"#{re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')}"
                    appendices[url] = (title, code)
            appendices_by_lang[lang] = appendices

        questions_by_lang: dict[str, List[tuple[str, List[str], List[str], List[List[str]]]]] = {}

        for lang, path in language_files.items():
            with open(path, encoding="utf-8") as f:
                content = f.read()
            # Remove appendix section for question parsing
            content_wo_appendix = re.split(r"^#\s*Anexos", content, maxsplit=1, flags=re.MULTILINE)[0]
            # Split only on lines that are exactly --- (with optional whitespace), not on --- inside tables
            raw_questions = [q for q in re.split(r'\n\s*---\s*\n', content_wo_appendix) if q.strip()]
            parsed: List[tuple[str, List[str], List[str], List[List[str]]]] = []
            # Remove leading/trailing empty lines from each block before splitting into lines
            for block in raw_questions:
                block = block.strip('\n')
                lines = block.split('\n')
                if not any(line.strip() for line in lines):
                    continue

                # Extract the statement (can span multiple lines until the first answer starts)
                statement_lines = []
                answer_lines = []
                metadata_lines = []
                is_answer_section = False
                is_metadata_section = False

                for line in lines:
                    if is_metadata_section:
                        if line.strip().startswith('|') and line.strip().endswith('|'):
                            metadata_lines.append(line)
                        else:
                            break
                    elif is_answer_section:
                        # Check if this line is the start of a metadata table
                        if line.strip().startswith('|') and line.strip().endswith('|'):
                            is_metadata_section = True
                            metadata_lines.append(line)
                        else:
                            answer_lines.append(line)
                    else:
                        if line.lstrip().startswith('- [X]') or (line.lstrip().startswith('-') and not line.lstrip().startswith('- [X]')):
                            is_answer_section = True
                            answer_lines.append(line)
                        else:
                            statement_lines.append(line)

                statement = '\n'.join(statement_lines).strip()

                # Process answers (can span multiple lines)
                correct: List[str] = []
                wrong: List[str] = []
                current_answer: list[str] = []
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

                # Parse metadata table if present
                metadata_table: List[List[str]] = []
                for line in metadata_lines:
                    if line.strip().startswith('|') and line.strip().endswith('|'):
                        row = [cell.strip() for cell in line.strip().strip('|').split('|')]
                        metadata_table.append(row)

                parsed.append((statement, correct, wrong, metadata_table))
            questions_by_lang[lang] = parsed

        question_count = len(next(iter(questions_by_lang.values())))
        for lang, questions in questions_by_lang.items():
            if len(questions) != question_count:
                raise ValueError(f"O número de preguntas en {lang} non coincide co resto.")

        toret: List[Question] = []
        for i in range(question_count):
            statements = {lang: questions_by_lang[lang][i][0] for lang in questions_by_lang}
            # Detect appendix reference in statement (e.g., [este anexo](#code-1))
            appendix_url = None
            appendix_title = None
            appendix_contents = {}
            # Find appendix reference in each language's statement
            appendix_urls_per_lang = {}
            for lang, statement in statements.items():
                match = re.search(r'\[.*?\]\((#code-[^)]+)\)', statement)
                if match:
                    appendix_urls_per_lang[lang] = match.group(1)
            # Only associate appendix if all languages reference the same appendix url
            if appendix_urls_per_lang and len(set(appendix_urls_per_lang.values())) == 1:
                appendix_url = next(iter(appendix_urls_per_lang.values()))
                for lang in questions_by_lang:
                    appendix = appendices_by_lang.get(lang, {}).get(appendix_url)
                    if appendix:
                        appendix_title, appendix_code = appendix
                        appendix_contents[lang] = appendix_code
            appendix_obj = None
            if appendix_contents:
                appendix_obj = Appendix(
                    title=appendix_title,
                    url=appendix_url,
                    content=MultilanguageString(appendix_contents)
                )

            corrects = {lang: questions_by_lang[lang][i][1] for lang in questions_by_lang}
            if len(set(len(corrects[lang]) for lang in corrects)) != 1:
                raise ValueError(f"Na pregunta {statements} non hai o mesmo número de respostas correctas en todos os idiomas.")
            wrongs = {lang: questions_by_lang[lang][i][2] for lang in questions_by_lang}
            if len(set(len(wrongs[lang]) for lang in wrongs)) != 1:
                raise ValueError(f"Na pregunta {statements} non hai o mesmo número de respostas incorrectas en todos os idiomas.")

            # Parse metadata for all languages
            metadatas = {lang: questions_by_lang[lang][i][3] for lang in questions_by_lang}
            metadata_dict: dict[str, dict[str, str]] = {}
            # If all languages have a metadata table with the same number of columns, parse it
            if all(metadatas[lang] and len(metadatas[lang]) >= 2 for lang in metadatas):
                # First row is header, second row is separator, rest are values
                for lang in metadatas:
                    table = metadatas[lang]
                    if len(table) < 3:
                        continue
                    keys = table[0]
                    values = table[2]  # Only one row of values supported for now
                    metadata_dict[lang] = {k: v for k, v in zip(keys, values)}
            else:
                # No metadata for this question
                for lang in metadatas:
                    metadata_dict[lang] = {}

            statement_ml = MultilanguageString(statements)
            correct_answers_ml = [MultilanguageString({lang: corrects[lang][j] for lang in corrects}) for j in range(len(next(iter(corrects.values()))))]
            wrong_answers_ml = [MultilanguageString({lang: wrongs[lang][j] for lang in wrongs}) for j in range(len(next(iter(wrongs.values()))))]

            toret.append(Question(statement_ml, correct_answers_ml, wrong_answers_ml, topics, metadata=metadata_dict, appendix=appendix_obj))

        return toret


if __name__ == "__main__":
    parser = MarkdownFolderParser()
    test_questions = parser.parse("test_data/all", topics=["topic1", "topic2"])
    for question in test_questions:
        if question.get_appendix():
            print(question.get_statement().get_translation("GL"))
            print(question.get_appendix().get_title())
            print(question.get_appendix().get_url())
            print(question.get_appendix().get_content())
    exit(0)
    for question in test_questions:
        print('*' * 20)
        print(question.get_statement().get_translation("GL"))
        print(len(question.get_right_answers()))
        print(len(question.get_wrong_answers()))
        print(question.get_right_answers()[0].get_translation("GL"))
        for q in question.get_wrong_answers():
            print('- ' + q.get_translation("GL"))
        print(question.get_topics())