# Markdown Question Bank

## Conda environment

```
conda env create -f environment.yml
conda activate markdown-question-bank
```

## Building quizes

Show the command help with: `python generate_quiz.py --help`

### Example 1 (without topics)

Generate two models with 6 questions each with the following command. Each model will have the same subsample of questions from the bank in the same order. The anwers will have a different order in each model (because of `--shuffle-answers`). 
 
```sh
export PYTHONPATH=src
python generate_quiz.py \
  --folder-path test_data/all \
  --outdir test_output \
  --num-models 2 \
  --num-questions 6 \
  --num-alternatives 3 \
  --shuffle-answers \
  --num-cols 3 \
  --lang GL \
  --seed 1234
```

### Example 2 (with topics)

Generate two models with 6 questions each with the following command. Each model will have the same subsample of questions from the bank in the same order. The anwers will have a different order in each model (because of `--shuffle-answers`). Questions are grouped by topic (because of `--group-by-topic`).
 
```sh
export PYTHONPATH=src
python generate_quiz.py \
  --folder-path test_data/bank \
  --outdir test_output \
  --num-models 2 \
  --num-questions 6 \
  --num-alternatives 3 \
  --shuffle-answers \
  --group-by-topic \
  --num-cols 3 \
  --lang GL \
  --seed 1234
```

## Building PDFs

After building your quizzes in an output directory (e.g., `outdir`), you can create PDFs using `generate_pdf.sh` (via `pandoc`, which is included in the conda environment). You will need:

- The input directory where all generated markdown files are located.
- A heading file to include in all generated PDFs.
- A CSS file to customize the output.

```sh
./generate_pdf.sh -d test_output -h test_files/head.md -c test_files/style.css
```

A PDF file for each markdown quiz will be placed alongside it.