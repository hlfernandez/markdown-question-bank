import os
from typing import List, Dict, Optional, Tuple, Dict, Any
from markdown_question_bank.question import Question, MultilanguageString, Appendix
import re

class MarkdownFolderParser:
    def parse(self, folder: str, topics: list[str] | None = None) -> List[Question]:
        """
        Parse markdown files in the specified folder and extract questions.
        
        Args:
            folder: Path to the folder containing markdown files
            topics: Optional list of topics to assign to all questions
            
        Returns:
            List of Question objects
        """
        if topics is None:
            topics = []
            
        # Get language files
        language_files = self._get_language_files(folder)
        
        # Parse appendices
        appendix_objects = self._parse_appendices(language_files)
        
        # Parse questions by language
        questions_by_lang = self._parse_questions_by_language(language_files)
        
        # Create Question objects
        return self._create_question_objects(questions_by_lang, appendix_objects, topics)
    
    def _get_language_files(self, folder: str) -> Dict[str, str]:
        """
        Get a dictionary mapping language codes to file paths.
        
        Args:
            folder: Path to the folder containing markdown files
            
        Returns:
            Dictionary mapping language codes to file paths
        """
        return {
            filename.split('.')[0].upper(): os.path.join(folder, filename)
            for filename in os.listdir(folder) if filename.endswith('.md')
        }
    
    def _parse_appendices(self, language_files: Dict[str, str]) -> Dict[int, Appendix]:
        """
        Parse appendices from language files.
        
        Args:
            language_files: Dictionary mapping language codes to file paths
            
        Returns:
            Dictionary mapping position to Appendix objects
        """
        # Parse appendices for each language
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
                appendices = self._extract_appendices_from_text(appendix_text, lang, appendix_positions)
                    
            appendices_by_lang[lang] = appendices
        
        # Now create MultilanguageString objects for titles, urls and contents
        return self._create_appendix_objects(appendix_positions)
    
    def _extract_appendices_from_text(self, 
                                     appendix_text: str, 
                                     lang: str, 
                                     appendix_positions: Dict[int, Dict[str, Tuple[str, str, str]]]) -> Dict[str, Tuple[str, str]]:
        """
        Extract appendices from text.
        
        Args:
            appendix_text: Text containing appendices
            lang: Language code
            appendix_positions: Dictionary to store appendix positions
            
        Returns:
            Dictionary mapping URL to (title, code) tuples
        """
        appendices = {}
        
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
            
        return appendices
    
    def _create_appendix_objects(self, appendix_positions: Dict[int, Dict[str, Tuple[str, str, str]]]) -> Dict[int, Appendix]:
        """
        Create Appendix objects from appendix positions.
        
        Args:
            appendix_positions: Dictionary mapping position to language data
            
        Returns:
            Dictionary mapping position to Appendix objects
        """
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
            
        return appendix_objects
    
    def _parse_questions_by_language(self, language_files: Dict[str, str]) -> Dict[str, List[Tuple[str, List[str], List[str], List[List[str]]]]]:
        """
        Parse questions from language files.
        
        Args:
            language_files: Dictionary mapping language codes to file paths
            
        Returns:
            Dictionary mapping language codes to lists of (statement, correct_answers, wrong_answers, metadata) tuples
        """
        questions_by_lang: dict[str, List[tuple[str, List[str], List[str], List[List[str]]]]] = {}

        for lang, path in language_files.items():
            with open(path, encoding="utf-8") as f:
                content = f.read()
                
            # Remove appendix section for question parsing
            content_wo_appendix = re.split(r"^#\s*(?:Anexos|Appendices)", content, maxsplit=1, flags=re.MULTILINE)[0]
            
            # Split only on lines that are exactly --- (with optional whitespace), not on --- inside tables
            raw_questions = [q for q in re.split(r'\n\s*---\s*\n', content_wo_appendix) if q.strip()]
            
            questions_by_lang[lang] = [self._parse_question_block(block) for block in raw_questions if block.strip()]
            
        self._validate_question_counts(questions_by_lang)
        
        return questions_by_lang
    
    def _validate_question_counts(self, questions_by_lang: Dict[str, List[Any]]) -> None:
        """
        Validate that all languages have the same number of questions.
        
        Args:
            questions_by_lang: Dictionary mapping language codes to lists of questions
            
        Raises:
            ValueError: If the number of questions is not the same for all languages
        """
        question_count = len(next(iter(questions_by_lang.values())))
        for lang, questions in questions_by_lang.items():
            if len(questions) != question_count:
                raise ValueError(f"O número de preguntas en {lang} non coincide co resto.")
    
    def _parse_question_block(self, block: str) -> Tuple[str, List[str], List[str], List[List[str]]]:
        """
        Parse a question block into statement, correct answers, wrong answers, and metadata.
        
        Args:
            block: Text block containing a question
            
        Returns:
            Tuple of (statement, correct_answers, wrong_answers, metadata)
        """
        block = block.strip('\n')
        lines = block.split('\n')
        if not any(line.strip() for line in lines):
            return '', [], [], []

        # Extract the statement, answers, and metadata sections
        statement_lines, answer_lines, metadata_lines = self._split_question_sections(lines)
        
        # Process the statement
        statement = '\n'.join(statement_lines).strip()
        
        # Process answers
        correct, wrong = self._parse_answers(answer_lines)
        
        # Parse metadata table
        metadata_table = self._parse_metadata(metadata_lines)
        
        return statement, correct, wrong, metadata_table
    
    def _split_question_sections(self, lines: List[str]) -> Tuple[List[str], List[str], List[str]]:
        """
        Split question lines into statement, answer, and metadata sections.
        
        Args:
            lines: List of lines in a question block
            
        Returns:
            Tuple of (statement_lines, answer_lines, metadata_lines)
        """
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
                    
        return statement_lines, answer_lines, metadata_lines
    
    def _parse_answers(self, answer_lines: List[str]) -> Tuple[List[str], List[str]]:
        """
        Parse answer lines into correct and wrong answers.
        
        Args:
            answer_lines: List of lines containing answers
            
        Returns:
            Tuple of (correct_answers, wrong_answers)
        """
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
                
        return correct, wrong
    
    def _parse_metadata(self, metadata_lines: List[str]) -> List[List[str]]:
        """
        Parse metadata lines into a table.
        
        Args:
            metadata_lines: List of lines containing metadata
            
        Returns:
            List of lists of strings representing the metadata table
        """
        metadata_table: List[List[str]] = []
        
        for line in metadata_lines:
            if line.strip().startswith('|') and line.strip().endswith('|'):
                row = [cell.strip() for cell in line.strip().strip('|').split('|')]
                metadata_table.append(row)
                
        return metadata_table
    
    def _create_question_objects(self, 
                               questions_by_lang: Dict[str, List[Tuple[str, List[str], List[str], List[List[str]]]]],
                               appendix_objects: Dict[int, Appendix],
                               topics: List[str]) -> List[Question]:
        """
        Create Question objects from parsed data.
        
        Args:
            questions_by_lang: Dictionary mapping language codes to lists of (statement, correct_answers, wrong_answers, metadata) tuples
            appendix_objects: Dictionary mapping position to Appendix objects
            topics: List of topics to assign to all questions
            
        Returns:
            List of Question objects
        """
        toret: List[Question] = []
        question_count = len(next(iter(questions_by_lang.values())))
        
        for i in range(question_count):
            # Gather statements, correct answers, and wrong answers from all languages
            statements = {lang: questions_by_lang[lang][i][0] for lang in questions_by_lang}
            corrects = {lang: questions_by_lang[lang][i][1] for lang in questions_by_lang}
            wrongs = {lang: questions_by_lang[lang][i][2] for lang in questions_by_lang}
            
            # Validate answer counts across languages
            self._validate_answer_counts(statements, corrects, wrongs)
            
            # Find appendix reference in statement
            question_appendix = self._find_question_appendix(statements, appendix_objects)
            
            # Parse metadata for all languages
            metadatas = {lang: questions_by_lang[lang][i][3] for lang in questions_by_lang}
            metadata_dict = self._parse_metadata_tables(metadatas)

            # Create multilanguage objects
            statement_ml = MultilanguageString(statements)
            correct_answers_ml = [MultilanguageString({lang: corrects[lang][j] for lang in corrects}) 
                                for j in range(len(next(iter(corrects.values()))))]
            wrong_answers_ml = [MultilanguageString({lang: wrongs[lang][j] for lang in wrongs}) 
                              for j in range(len(next(iter(wrongs.values()))))]

            # Create Question object
            toret.append(Question(
                statement_ml, 
                correct_answers_ml, 
                wrong_answers_ml, 
                topics, 
                metadata=metadata_dict, 
                appendix=question_appendix
            ))
            
        return toret
    
    def _validate_answer_counts(self, 
                              statements: Dict[str, str], 
                              corrects: Dict[str, List[str]], 
                              wrongs: Dict[str, List[str]]) -> None:
        """
        Validate that all languages have the same number of correct and wrong answers.
        
        Args:
            statements: Dictionary mapping language codes to statements
            corrects: Dictionary mapping language codes to lists of correct answers
            wrongs: Dictionary mapping language codes to lists of wrong answers
            
        Raises:
            ValueError: If the number of answers is not the same for all languages
        """
        if len(set(len(corrects[lang]) for lang in corrects)) != 1:
            raise ValueError(f"Na pregunta {statements} non hai o mesmo número de respostas correctas en todos os idiomas.")
            
        if len(set(len(wrongs[lang]) for lang in wrongs)) != 1:
            raise ValueError(f"Na pregunta {statements} non hai o mesmo número de respostas incorrectas en todos os idiomas.")
    
    def _find_question_appendix(self, statements: Dict[str, str], appendix_objects: Dict[int, Appendix]) -> Optional[Appendix]:
        """
        Find appendix referenced in the statement.
        
        Args:
            statements: Dictionary mapping language codes to statements
            appendix_objects: Dictionary mapping position to Appendix objects
            
        Returns:
            Appendix object referenced in the statement, or None
        """
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
                    
        return question_appendix
    
    def _parse_metadata_tables(self, metadatas: Dict[str, List[List[str]]]) -> Dict[str, Dict[str, str]]:
        """
        Parse metadata tables for all languages.
        
        Args:
            metadatas: Dictionary mapping language codes to metadata tables
            
        Returns:
            Dictionary mapping language codes to dictionaries of metadata key-value pairs
        """
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
                
        return metadata_dict


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

    for question in test_questions:
        print('*' * 20)
        print(question.get_statement().get_translation("GL"))
        print(len(question.get_right_answers()))
        print(len(question.get_wrong_answers()))
        print(question.get_right_answers()[0].get_translation("GL"))
        for q in question.get_wrong_answers():
            print('- ' + q.get_translation("GL"))
        print(question.get_topics())