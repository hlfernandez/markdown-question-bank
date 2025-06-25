from typing import Dict, List, Optional

class MultilanguageString:
    def __init__(self, translations: Optional[Dict[str, str]] = None):
        self.translations = translations or {}

    def get_languages(self) -> List[str]:
        return list(self.translations.keys())

    def get_translation(self, language: str) -> str:
        return self.translations.get(language, "")

    def add_translation(self, language: str, text: str):
        self.translations[language] = text

    def __str__(self) -> str:
        return self.translations.__str__()

    def __eq__(self, other):
        if not isinstance(other, MultilanguageString):
            return False
        return self.translations == other.translations
    
    def __hash__(self):
        return hash(tuple(sorted(self.translations.items())))

class Appendix:
    def __init__(self, title: Optional[MultilanguageString] = None, url: Optional[MultilanguageString] = None, content: Optional[MultilanguageString] = None):
        self.title = title if title is not None else MultilanguageString()
        self.url = url if url is not None else MultilanguageString()
        self.content = content if content is not None else MultilanguageString()

    def get_title(self, language: Optional[str] = None) -> str:
        if language is None:
            lang = self.title.get_languages()[0] if self.title.get_languages() else ""
            return self.title.get_translation(lang)
        return self.title.get_translation(language)

    def get_url(self, language: Optional[str] = None) -> str:
        if language is None:
            lang = self.url.get_languages()[0] if self.url.get_languages() else ""
            return self.url.get_translation(lang)
        return self.url.get_translation(language)

    def get_content(self) -> MultilanguageString:
        return self.content

    def __eq__(self, other):
        if not isinstance(other, Appendix):
            return False
        return (self.title, self.url, self.content) == (other.title, other.url, other.content)

    def __hash__(self):
        return hash((str(self.title), str(self.url), str(self.content)))
    
    def __str__(self) -> str:
        return f"Appendix(title={self.title}, url={self.url})"
    
    def __repr__(self) -> str:
        return self.__str__()

class Question:
    def __init__(
        self,
        statement: MultilanguageString,
        correct_answers: List[MultilanguageString],
        wrong_answers: List[MultilanguageString],
        topics: List[str],
        metadata: dict[str, dict[str, str]] | None = None,
        appendix: Appendix | None = None
    ):
        self.statement = statement
        self.correct_answers = correct_answers
        self.wrong_answers = wrong_answers
        self.topics = topics
        self.metadata = metadata if metadata is not None else {}
        self.appendix = appendix

    def get_languages(self) -> List[str]:
        return self.statement.get_languages()

    def get_statement(self) -> MultilanguageString:
        return self.statement

    def get_topics(self) -> List[str]:
        return self.topics

    def get_right_answers(self) -> List[MultilanguageString]:
        return self.correct_answers

    def get_wrong_answers(self) -> List[MultilanguageString]:
        return self.wrong_answers

    def get_metadata(self) -> Dict[str, Dict[str, str]]:
        return self.metadata

    def get_appendix(self) -> 'Appendix | None':
        return self.appendix
