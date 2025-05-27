import sys
from pfylter.core import NotFilter, AnyFilter
from markdown_question_bank.parser_bank import BankFolderParser
from markdown_question_bank.bank_filtered import MetadataQuestionFilter, FilteredBank

def create_filters(exclude_metadata):
    """
    Create a list of filters based on the exclude_metadata option.
    Each filter is created from a CLI argument in the format "language:metadata_key:metadata_value".
    """
    filters = []
    for arg in exclude_metadata:
        try:
            filters.append(MetadataQuestionFilter.from_cli_args(arg))
        except ValueError as e:
            print(f"Error parsing filter argument '{arg}': {e}")
            sys.exit(1)
    return filters


def create_bank(folder_path, num_alternatives, exclude_topic=None, exclude_metadata=None, verbose=True):
    parser = BankFolderParser(min_wrong=num_alternatives - 1)
    bank = parser.parse(folder_path)

    if exclude_topic:
        exclude_topics = list(exclude_topic)
        if verbose:
            print(f"Excluding topics: {', '.join(exclude_topics)}")
        bank = bank.filter_topics(exclude_topics)

    if exclude_metadata:
        if verbose:
            print(f"Excluding metadata: {', '.join(exclude_metadata)}")
        bank = FilteredBank(bank, NotFilter(AnyFilter(create_filters(exclude_metadata))))

    return bank
