import click
from markdown_question_bank.cli_utils import create_bank

@click.command()
@click.option('--folder-path', required=True, type=click.Path(exists=True), help='Path to the folder containing the question bank.')
@click.option('--num-alternatives', default=4, help='Number of alternatives per question.')
@click.option('--exclude-topic', multiple=True, help='Topic(s) to exclude from the question bank. Can be specified multiple times.')
@click.option('--exclude-metadata', multiple=True, help='Metadata fields to exclude from the question bank. Can be specified multiple times.')
def bank_summary(folder_path, num_alternatives, exclude_topic, exclude_metadata):
    bank = create_bank(folder_path, num_alternatives, exclude_topic, exclude_metadata)

    num_questions = len(bank.get_questions())
    languages = bank.get_languages() if hasattr(bank, 'get_languages') else []
    topics = bank.get_topics() if hasattr(bank, 'get_topics') else []
    topics.sort()

    print(f"Number of questions: {num_questions}")
    print(f"Available languages: {', '.join(languages) if languages else 'NA'}")
    if topics:
        print(f"Available topics: {', '.join(topics) if topics else 'NA'}")

        print("Number of questions by topic:")
        for topic in topics:
            count = len(bank.get_questions_by_topic(topic))
            print(f"  - {topic}: {count}")

if __name__ == '__main__':
    bank_summary()
