from typing import Dict, List

class MultilanguageString:
    def __init__(self, translations: Dict[str, str]):
        self.translations = translations

    def get_languages(self) -> List[str]:
        return list(self.translations.keys())

    def get_translation(self, language: str) -> str:
        return self.translations[language]

    def __str__(self) -> str:
        return self.translations.__str__()

class Appendix:
    def __init__(self, title: str, url: str, content: MultilanguageString):
        self.title = title
        self.url = url
        self.content = content

    def get_title(self) -> str:
        return self.title

    def get_url(self) -> str:
        return self.url

    def get_content(self) -> MultilanguageString:
        return self.content

    def __eq__(self, other):
        if not isinstance(other, Appendix):
            return False
        return (self.title, self.url, str(self.content)) == (other.title, other.url, str(other.content))

    def __hash__(self):
        return hash((self.title, self.url, str(self.content)))
    
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
