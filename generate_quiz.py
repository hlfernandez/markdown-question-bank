import os
import click
from markdown_question_bank.parser_bank import BankFolderParser
from markdown_question_bank.sampler_question import CachedQuestionSampler, RandomQuestionSampler, TopicQuestionSampler
from markdown_question_bank.sampler_answers import DefaultAnswerStrategySelector, CachedAnswerSampler, DefaultAnswerSampler
from markdown_question_bank.quiz_builder import QuizBuilder
from markdown_question_bank.quiz_markdown_exporter import QuizExporter

@click.command()
@click.option('--folder-path', required=True, type=click.Path(exists=True), help='Path to the folder containing the question bank.')
@click.option('--outdir', default='output', type=click.Path(), help='Directory to save the generated quiz models.')
@click.option('--num-models', default=2, help='Number of quiz models to generate.')
@click.option('--num-questions', default=6, help='Number of questions per model.')
@click.option('--num-alternatives', default=4, help='Number of alternatives per question.')
@click.option('--num-cols', default=3, help='Number of columns in the answer table.')
@click.option('--lang', default=None, help='Single language to export (GL, ES, EN...). By default, exports all available languages.')
@click.option('--seed', default=2025, help='Random seed for reproducibility.')
@click.option('--shuffle-answers', is_flag=True, default=False, help='Shuffle the answers for each question.')
@click.option('--shuffle-questions', is_flag=True, default=False, help='Shuffle the questions in each model.')
@click.option('--group-by-topic', is_flag=True, default=False, help='Group questions by topic.')
@click.option('--exclude-topic', multiple=True, help='Topic(s) to exclude from the question bank. Can be specified multiple times.')
@click.option('--equal-questions-per-topic', is_flag=True, default=False, help='Force the same number of questions per topic. If a topic does not have enough questions, the remaining will be taken randomly from other topics.')
def generate_quizzes(folder_path, outdir, num_models, num_questions, num_alternatives, num_cols, lang, seed, shuffle_answers, shuffle_questions, group_by_topic, exclude_topic, equal_questions_per_topic):
    os.makedirs(outdir, exist_ok=True)

    parser = BankFolderParser(min_wrong=num_alternatives - 1)
    bank = parser.parse(folder_path)

    if exclude_topic:
        bank = bank.filter_topics(list(exclude_topic))

    if equal_questions_per_topic:
        question_sampler = CachedQuestionSampler(TopicQuestionSampler.from_bank(bank, num_questions, seed))
    else:
        question_sampler = CachedQuestionSampler(RandomQuestionSampler(num_questions, seed))

    answer_sampler = CachedAnswerSampler(DefaultAnswerSampler())
    answer_strategy = DefaultAnswerStrategySelector(answer_sampler)

    quiz = QuizBuilder(
        bank=bank,
        num_models=num_models,
        question_sampler=question_sampler,
        answer_strategy_selector=answer_strategy,
        num_alternatives=num_alternatives,
        seed=seed,
        shuffle_answers=shuffle_answers,
        shuffle_questions=shuffle_questions,
        group_by_topic=group_by_topic
    )

    models = quiz.build_models()
    languages = [lang] if lang else bank.languages

    exporter = QuizExporter(outdir, num_cols)
    generated_files = exporter.export_models(models, languages)

    click.echo("Output files:")
    for path in generated_files:
        click.echo(f" - {path}")


if __name__ == '__main__':
    generate_quizzes()
