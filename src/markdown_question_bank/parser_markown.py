import os
from typing import List, Dict, Optional
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
        # First, collect all appendices for each language and position
        appendix_positions: dict[int, dict[str, tuple[str, str, str]]] = {}  # Mapping of position -> {lang: (title, code, url)}

        for lang, path in language_files.items():
            with open(path, encoding="utf-8") as f:
                content = f.read()
            # Find appendix section
            appendix_section = re.search(r"^#\s*(?:Anexos|Appendices)(.+)$", content, re.DOTALL | re.MULTILINE)

            appendices = {}
            if appendix_section:
                appendix_text = appendix_section.group(1)
                # Split by appendix headings (## ...), keep heading in result
                appendix_blocks = re.split(r'(^##\s+.+$)', appendix_text, flags=re.MULTILINE)
                # The split will result in ['', '## Title1', '...content1...', '## Title2', '...content2...', ...]
                for i in range(1, len(appendix_blocks), 2):
                    position = i//2  # Position 0, 1, 2, etc. for each appendix
                    heading = appendix_blocks[i].strip()
                    content_block = appendix_blocks[i+1] if (i+1) < len(appendix_blocks) else ''
                    title = heading[2:].strip()
                    code = content_block.strip('\n')
                    
                    # Generate URL from title consistently for all languages
                    # Keep accents and other Unicode characters in URLs
                    url = f"#{title.lower().replace(' ', '-')}"
                        
                    appendices[url] = (title, code)

                    
                    # Store by position for cross-language mapping
                    if position not in appendix_positions:
                        appendix_positions[position] = {}
                    appendix_positions[position][lang] = (title, code, url)
                    
            appendices_by_lang[lang] = appendices
        
        # Now create MultilanguageString objects for titles, urls and contents
        appendix_objects = {}  # Position -> Appendix object
        for position, lang_data in appendix_positions.items():
            title_ml = MultilanguageString({})
            url_ml = MultilanguageString({})
            content_ml = MultilanguageString({})
            
            for lang, (title, code, url) in lang_data.items():
                title_ml.add_translation(lang, title)
                url_ml.add_translation(lang, url)
                content_ml.add_translation(lang, code)
            
            appendix_obj = Appendix(title=title_ml, url=url_ml, content=content_ml)
            appendix_objects[position] = appendix_obj

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
            # Detect appendix reference in statement (e.g., [este anexo](#exceptions))
            question_appendix: Optional[Appendix] = None
            # Find appendix reference in each language's statement
            appendix_urls_per_lang = {}
            # First, collect appendix URLs from each language's statement
            for lang, statement in statements.items():
                match = re.search(r'\[.*?\]\((#[^)]+)\)', statement)
                if match:
                    url = match.group(1)
                    appendix_urls_per_lang[lang] = url
            
            # If we found references in the statements
            if appendix_urls_per_lang:
                # Look through all appendix objects to find the one that matches by URL in each language
                for pos, app_obj in appendix_objects.items():
                    matches = True
                    for lang, url in appendix_urls_per_lang.items():
                        if lang in app_obj.url.translations and app_obj.url.get_translation(lang) == url:
                            continue
                        else:
                            matches = False
                            break
                    
                    if matches:
                        question_appendix = app_obj
                        break

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

            toret.append(Question(statement_ml, correct_answers_ml, wrong_answers_ml, topics, metadata=metadata_dict, appendix=question_appendix))

        return toret


if __name__ == "__main__":
    parser = MarkdownFolderParser()
    test_questions = parser.parse("test_data/all", topics=["topic1", "topic2"])
    for question in test_questions:
        appendix = question.get_appendix()
        if appendix:
            print(question.get_statement().get_translation("GL"))
            print(f"Title (GL): {appendix.get_title('GL')}")
            print(f"URL (GL): {appendix.get_url('GL')}")
            print(f"Content: {appendix.get_content().get_translation('GL')[:50]}...")
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