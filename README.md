# Markdown Question Bank

Show the command help with: `python generate_quiz.py --help`

Generate two models with 6 questions each with the following command. Each model will have the same subsample of questions from the bank in the same order. The anwers will have a different order in each model (because of the `--shuffle-answers`). 
 
```sh
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