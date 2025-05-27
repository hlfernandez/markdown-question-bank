import click
from markdown_question_bank.parser_bank import BankFolderParser
from markdown_question_bank.bank_filtered import MetadataQuestionFilter, FilteredBank
from pfylter.core import NotFilter, AnyFilter

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
            exit(1)
    return filters

@click.command()
@click.option('--folder-path', required=True, type=click.Path(exists=True), help='Path to the folder containing the question bank.')
@click.option('--num-alternatives', default=4, help='Number of alternatives per question.')
@click.option('--exclude-topic', multiple=True, help='Topic(s) to exclude from the question bank. Can be specified multiple times.')
@click.option('--exclude-metadata', multiple=True, help='Metadata fields to exclude from the question bank. Can be specified multiple times.')
def bank_summary(folder_path, num_alternatives, exclude_topic, exclude_metadata):
    parser = BankFolderParser(min_wrong=num_alternatives - 1)
    bank = parser.parse(folder_path)

    if exclude_topic:
        exclude_topics = list(exclude_topic)
        print(f"Excluíndo temas: {', '.join(exclude_topics)}")
        bank = bank.filter_topics(exclude_topics )

    if exclude_metadata:
        print(f"Excluíndo metadatos: {', '.join(exclude_metadata)}")
        bank = FilteredBank(bank, NotFilter(AnyFilter(create_filters(exclude_metadata))))

    num_questions = len(bank.get_questions())
    languages = bank.get_languages() if hasattr(bank, 'get_languages') else []
    topics = bank.get_topics() if hasattr(bank, 'get_topics') else []
    topics.sort()

    print(f"Número de preguntas: {num_questions}")
    print(f"Idiomas dispoñibles: {', '.join(languages) if languages else 'Descoñecido'}")
    print(f"Temas dispoñibles: {', '.join(topics) if topics else 'Descoñecido'}")

    if topics:
        print("Preguntas por tema:")
        for topic in topics:
            count = len(bank.get_questions_by_topic(topic))
            print(f"  - {topic}: {count}")

if __name__ == '__main__':
    bank_summary()
