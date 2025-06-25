from typing import List, Optional
from pfylter.core import AbstractFilter, AllFilters, AnyFilter, NotFilter
from markdown_question_bank.bank import Bank
from markdown_question_bank.question import Question


class MetadataQuestionFilter(AbstractFilter[Question]):

    def __init__(self, language: str, metadata_key: str, metadata_value: str):
        self.language = language
        self.metadata_key = metadata_key
        self.metadata_value = metadata_value
    
    def keep(self, instance: Question) -> bool:
        if self.language not in instance.get_languages():
            return False
        
        metadata = instance.get_metadata().get(self.language, {})
        if self.metadata_key in metadata and metadata[self.metadata_key] == self.metadata_value:
            return True
        
        return False

    @staticmethod
    def from_cli_args(cli_arg: str) -> 'MetadataQuestionFilter':
        """
        Create a MetadataQuestionFilter from a CLI argument string.
        The expected format is "language:metadata_key:metadata_value".
        """
        parts = cli_arg.split(':')
        if len(parts) != 3:
            raise ValueError("CLI argument must be in the format 'language:metadata_key:metadata_value'")
        
        language, metadata_key, metadata_value = parts
        return MetadataQuestionFilter(language, metadata_key, metadata_value)


class FilteredBank:
    def __init__(self, bank: Bank, question_filter: AbstractFilter[Question]):
        self._filtered_bank = Bank(
            question_filter.apply(bank.get_questions()), bank.get_min_wrong()
        )

    def get_questions(self) -> List[Question]:
        return self._filtered_bank.get_questions()

    def get_topics(self) -> List[str]:
        return self._filtered_bank.get_topics()

    def get_questions_by_topic(self, topic: str) -> List[Question]:
        return self._filtered_bank.get_questions_by_topic(topic)

    def filter_topics(self, topics: Optional[List[str]] = None) -> 'Bank':
        return self._filtered_bank.filter_topics(topics)
    
    def get_languages(self) -> List[str]:
        return self._filtered_bank.get_languages()
    
if __name__ == "__main__":
    from markdown_question_bank.parser_markown import MarkdownFolderParser

    parser = MarkdownFolderParser()
    test_questions = parser.parse("test_data/all", topics=["topic1", "topic2"])
    bank = Bank(test_questions, min_wrong=2)
    
    print(f"Total questions: {len(bank.get_questions())}")

    class QuickTestQuestionFilter(AbstractFilter[Question]):
        def keep(self, question: Question) -> bool:
            return question.get_metadata().get('ES').get('Dificultad', 'easy') == 'Alta'

    filtered = FilteredBank(bank, AllFilters([QuickTestQuestionFilter()]))

    print(f"Total questions: {len(filtered.get_questions())}")

    cli_filters = [
        MetadataQuestionFilter.from_cli_args('ES:Dificultad:Alta'),
        MetadataQuestionFilter.from_cli_args('ES:TeachScore:1')
    ]
    filtered = FilteredBank(bank, NotFilter(AnyFilter(cli_filters)))

    print(f"Total questions: {len(filtered.get_questions())}")