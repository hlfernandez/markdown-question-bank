# 📝 Markdown Question Bank

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A flexible, multilingual, and scriptable question bank system for building quizzes and generating printable PDFs from Markdown.**

---

## 📋 Table of contents

- [📦 Features](#-features)
- [🛠️ Getting Started](#-getting-started)
    - [🐍 Conda Environment](#-conda-environment)
- [🗂️ Questions Format](#-questions-format)
    - [ℹ️ Metadata](#-metadata)
    - [📄 Code Appendices](#-code-appendices)
- [📊 Bank Information](#-bank-information)
    - [🧲 Filters](#%F0%9F%A7%B2-filters)
- [🏗️ Building Quizzes](#-building-quizzes)
    - [✨ Example 1: Without Topics](#-example-1-without-topics)
    - [🗃️ Example 2: With Topics](#-example-2-with-topics)
- [🖨️ Building PDFs](#-building-pdfs)
    - [🧪 Advanced: Jinja2 Headings](#%F0%9F%A7%AA-advanced-jinja2-headings)
- [👨‍💻 Developers](#%E2%80%8D-developers)
    - [🔄 Updating Version](#-updating-version)
    - [🧪 Running Tests](#%F0%9F%A7%AA-running-tests)
- [👥 Contributors](#-contributors)
- [🤝 Contributing](#-contributing)

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

## 🗂️ Questions Format

The bank of questions consists of one or several Markdown files that can be optionally organized in subfolders that act as topics. Within each file, questions are written in Markdown and separated by `---`. The right answer is marked with an `[X]` at the beginning, right after the list symbol. Here is a sample question:

```markdown
What is the result of `len("Python")`?

- 5
- [X] 6
- 7
```

### ℹ️ Metadata

Optionally, a question may include a metadata table after the list of possible choices. For instance, the following question will be associated to `Difficulty = Low` and `TeachScore = 2`.
```markdown
What is the result of `len("Python")`?

- 5
- [X] 6
- 7

| Difficulty  | TeachScore |
|-------------|------------|
| Low         | 2          |
```
These metadata keys can be used later for excluding questions with the `--exclude-metadata` option or to implement other custom filterings or groupings.

### 📄 Code Appendices

Several questions may refer to the same piece of code. To avoid repeating it across them and having long quizzes, code appendices can be created at the end of each Markdown file as follows:

````markdown
# Appendices

## Code 1

```python
def misterio(x):
    return x[::-1]

print(misterio("abc"))
```
````

And then the appendix is referred in the question as follows:
```markdown
Given the Python code from [this appendix](#code-1), indicate what its behavior and console output would be:

- [X] The function reverses the string.
  The output would be: `cba`.
- The function removes the first letter and prints the remaining string.
  The output would be: `bc`.
- The function transforms the string to uppercase.
  The output would be: `ABC`.
```

This way, if the question is included in the bank and sampled for building a quiz, the corresponding appendix will be added at the end of the quiz.

---

## 📊 Bank Information

Use the `bank_summary.py` command to get a summary of the bank:

```sh
export PYTHONPATH=src
python bank_summary.py \
  --folder-path test_data/bank \
  --num-alternatives 3
```

### 🧲 Filters

This command allows two filters (also available in the `generate_quiz.py` command):

- `--exclude-topic`: Topic(s) to exclude from the question bank. Can be specified multiple times.
- `--exclude-metadata`: Metadata fields to exclude from the question bank. Can be specified multiple times. It must follow the following format: `<language>:<field_name>:<value>`.

---

## 🏗️ Building Quizzes

Show the command help with: 

```sh
export PYTHONPATH=src
python generate_quiz.py --help
```

**Interesting flags:**
- `--equal-questions-per-topic`: Distributes the total number of questions as evenly as possible across all topics. If a topic does not have enough available questions, the remaining questions are taken from other topics with more questions.
- `--group-by-topic`: Groups questions by topic. Otherwise questions appear in a random order.

Below are provided some examples of this command.

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

## 👨‍💻 Developers

### 🔄 Updating Version

The project includes a script to update the version across all relevant files:

```sh
./update_version.sh <new_version>
```

For example:
```sh
./update_version.sh 1.2.0
```

### 🧪 Running Tests

To run the test suite:

```sh
conda activate markdown-question-bank
pytest
```

Or to run a specific test file:

```sh
conda activate markdown-question-bank
pytest tests/test_parser_bank.py -s
```

---

## 👥 Contributors

<a href="https://github.com/hlfernandez/markdown-question-bank/">
  <img src="https://contrib.rocks/image?repo=hlfernandez/markdown-question-bank"/>
</a>

<sup>Made with [contrib.rocks](https://contrib.rocks).</sup>

---

## 🤝 Contributing

Pull requests and suggestions are welcome! Feel free to open an issue or submit a PR.

---
