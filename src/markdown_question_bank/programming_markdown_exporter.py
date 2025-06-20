import os
from datetime import datetime

class ProgrammingMarkdownExporter:
    def __init__(self, outdir: str):
        self.outdir = outdir
        os.makedirs(outdir, exist_ok=True)
        self.translations = {
            'EN': {'Question': 'Question', 'Score': 'Score'},
            'ES': {'Question': 'Pregunta', 'Score': 'Puntuación'},
            'GL': {'Question': 'Pregunta', 'Score': 'Puntuación'}
        }

    def get_timestamped_dir(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamped_dir = os.path.join(self.outdir, timestamp)
        os.makedirs(timestamped_dir, exist_ok=True)

        return timestamped_dir

    def export_models(self, programming_bank, programming_models, languages):
        generated_files = []
        current_outdir = self.get_timestamped_dir()
        for model_idx, model in enumerate(programming_models):
            for lang in languages:
                filename = ProgrammingMarkdownExporter._get_filename(current_outdir, model_idx, lang)
                with open(filename, 'w', encoding='utf-8') as f:
                    self._write_model(f, model, programming_bank, lang)
                generated_files.append(filename)
        return generated_files

    @staticmethod
    def _get_filename(outdir, model_idx, lang):
        return os.path.join(outdir, f"model_{model_idx+1}_{lang}.md")

    def _write_model(self, file_handle, model, programming_bank, lang):
        for idx, qinfo in enumerate(model.questions):
            qnum = str(idx + 1)
            problem = self._find_problem(programming_bank, qinfo.dir)
            if not problem:
                raise ValueError(f"Problem for question {qnum} not found in the programming bank.")
            statement = problem.get_statement().get_translation(lang)
            file_handle.write(f"**{self.translations[lang]['Question']} {qnum}**. [{self.translations[lang]['Score']}: {qinfo.score}] {statement}\n\n")

    def _find_problem(self, programming_bank, dir_name):
        return next((p for p in programming_bank.get_problems() if p.get_title() == dir_name), None)
