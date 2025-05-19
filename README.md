# Markdown Question Bank

## Conda environment

```
conda env create -f environment.yml
conda activate markdown-question-bank
```

## Bank information

Use the `bank_summary.py` command to get a summary of the bank:

```sh
export PYTHONPATH=src
python bank_summary.py --folder-path test_data/bank --num-alternatives 3
```

## Building quizes

Show the command help with: `python generate_quiz.py --help`.

Interesting flags are:
- `--equal-questions-per-topic`: Distributes the total number of questions as evenly as possible across all topics. The total number of questions is divided by the number of topics to determine how many to select from each. If a topic does not have enough available questions, the remaining questions are taken from other topics with more questions.

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

If you want that your heading file be different in someway, we facilitate the use of Jinja2 in your heading files. By now, the `filename` variable will be available inside your Jinja2 heading template (check out `test_files/head.jinja2`).

```sh
./generate_pdf.sh -d test_output -h test_files/head.jinja2 -c test_files/style.css
```
