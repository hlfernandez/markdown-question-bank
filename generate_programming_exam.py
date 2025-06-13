import click
from markdown_question_bank.parser_programming_bank import ProgrammingBankParser
from markdown_question_bank.programming_models import ProgrammingModels
from markdown_question_bank.programming_markdown_exporter import ProgrammingMarkdownExporter

@click.command()
@click.option('--folder-path', required=True, type=click.Path(exists=True), help='Path to the folder containing the programming bank.')
@click.option('--outdir', required=True, type=click.Path(), help='Directory to save the generated exam files.')
@click.option('--models-config', required=True, type=click.Path(exists=True), help='Path to the JSON file with the models configuration.')
@click.option('--lang', default=None, help='Single language to export (GL, ES, EN...). By default, exports all available languages.')
def generate_programming_exam(folder_path, outdir, models_config, lang):
    parser = ProgrammingBankParser(folder_path)
    programming_bank = parser.parse()
    languages = [lang] if lang else programming_bank.get_languages()

    programming_models = ProgrammingModels.from_json(models_config)
    exporter = ProgrammingMarkdownExporter(outdir)
    generated_files = exporter.export_models(programming_bank, programming_models, languages)
    click.echo("Output files:")
    for path in generated_files:
        click.echo(f" - {path}")

if __name__ == '__main__':
    generate_programming_exam()
