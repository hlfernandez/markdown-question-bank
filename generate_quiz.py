import os
import click
from markdown_question_bank.parser_bank import BankFolderParser
from markdown_question_bank.sampler_question import CachedQuestionSampler, RandomQuestionSampler
from markdown_question_bank.sampler_answers import DefaultAnswerStrategySelector, CachedAnswerSampler, DefaultAnswerSampler
from markdown_question_bank.quiz_builder import QuizBuilder
from markdown_question_bank.quiz_markdown_exporter import QuizExporter

@click.command()
@click.option('--folder-path', required=True, type=click.Path(exists=True), help='Ruta ao cartafol co banco de preguntas.')
@click.option('--outdir', default='output', type=click.Path(), help='Cartafol onde gardar os modelos xerados.')
@click.option('--num-models', default=2, help='Número de modelos a xerar.')
@click.option('--num-questions', default=6, help='Número de preguntas por modelo.')
@click.option('--num-alternatives', default=4, help='Número de alternativas por pregunta.')
@click.option('--num-cols', default=3, help='Número de columnas na táboa de respostas.')
@click.option('--lang', default=None, help='Idioma único a exportar (GL, ES, EN...). Por defecto, exporta todos os dispoñibles.')
@click.option('--seed', default=2025, help='Semente aleatoria para reproducibilidade.')
@click.option('--shuffle-answers', is_flag=True, default=False, help='Indica se as respostas deben ser baralladas.')
@click.option('--shuffle-questions', is_flag=True, default=False, help='Indica se as preguntas deben ser baralladas.')
def generate_quizzes(folder_path, outdir, num_models, num_questions, num_alternatives, num_cols, lang, seed, shuffle_answers, shuffle_questions):
    os.makedirs(outdir, exist_ok=True)

    parser = BankFolderParser(min_wrong=num_alternatives - 1)
    bank = parser.parse(folder_path)

    question_sampler = CachedQuestionSampler(RandomQuestionSampler(num_questions))
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
        shuffle_questions=shuffle_questions
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
