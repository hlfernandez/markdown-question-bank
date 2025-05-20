import click
from markdown_question_bank.parser_bank import BankFolderParser

@click.command()
@click.option('--folder-path', required=True, type=click.Path(exists=True), help='Path to the folder containing the question bank.')
@click.option('--num-alternatives', default=4, help='Number of alternatives per question.')
@click.option('--exclude-topic', multiple=True, help='Topic(s) to exclude from the question bank. Can be specified multiple times.')
def bank_summary(folder_path, num_alternatives, exclude_topic):
    parser = BankFolderParser(min_wrong=num_alternatives - 1)
    bank = parser.parse(folder_path)

    if exclude_topic:
        bank = bank.filter_topics(list(exclude_topic))

    num_questions = len(bank.get_questions())
    languages = bank.languages if hasattr(bank, 'languages') else []
    topics = bank.get_topics() if hasattr(bank, 'get_topics') else []

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
