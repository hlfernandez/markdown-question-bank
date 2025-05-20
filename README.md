# 📝 Markdown Question Bank

> **A flexible, multilingual, and scriptable question bank system for building quizzes and generating printable PDFs from Markdown.**

---

## 📦 Features

- 🗂️ Organize questions by topic using folders
- 🌐 Multilingual support for questions and answers
- 🔀 Shuffle answers and questions for randomized quizzes
- 🏷️ Group questions by topic or distribute evenly
- 🖨️ Generate printable PDFs with custom headings and styles
- 🧩 Jinja2 templating for dynamic PDF headings

---

## 🛠️ Getting Started

### 🐍 Conda Environment

```sh
conda env create -f environment.yml
conda activate markdown-question-bank
```

---

## 📊 Bank Information

Use the `bank_summary.py` command to get a summary of the bank:

```sh
export PYTHONPATH=src
python bank_summary.py --folder-path test_data/bank --num-alternatives 3
```

---

## 🏗️ Building Quizzes

Show the command help with: 

```sh
export PYTHONPATH=src
python generate_quiz.py --help
```

**Interesting flags:**
- `--equal-questions-per-topic`: Distributes the total number of questions as evenly as possible across all topics. If a topic does not have enough available questions, the remaining questions are taken from other topics with more questions.

### ✨ Example 1: Without Topics

Generate two models with 6 questions each. Each model will have the same subsample of questions from the bank in the same order. The answers will have a different order in each model (because of `--shuffle-answers`).

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

### 🗃️ Example 2: With Topics

Generate two models with 6 questions each, grouped by topic (because of `--group-by-topic`):

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

---

## 🖨️ Building PDFs

After building your quizzes in an output directory (e.g., `outdir`), you can create PDFs using `generate_pdf.sh` (via `pandoc`, which is included in the conda environment). 

You will need:
- 📁 The input directory where all generated markdown files are located.
- 🏷️ A heading file to include in all generated PDFs.
- 🎨 A CSS file to customize the output.

```sh
./generate_pdf.sh -d test_output -h test_files/head.md -c test_files/style.css
```

A PDF file for each markdown quiz will be placed alongside it.

### 🧪 Advanced: Jinja2 Headings

If you want your heading file to be dynamic, you can use Jinja2 in your heading files. The `filename` variable will be available inside your Jinja2 heading template (see `test_files/head.jinja2`):

```sh
./generate_pdf.sh -d test_output -h test_files/head.jinja2 -c test_files/style.css
```

---

## 🤝 Contributing

Pull requests and suggestions are welcome! Feel free to open an issue or submit a PR.

---
