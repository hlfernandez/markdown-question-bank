from typing import List
import random
from markdown_question_bank.quiz_model import QuizModel, QuizQuestion
from markdown_question_bank.bank import Bank
from markdown_question_bank.sampler_question import QuestionSampler
from markdown_question_bank.sampler_answers import AnswerStrategySelector

class QuizBuilder:
    def __init__(
        self,
        bank: Bank,
        num_models: int,
        question_sampler: QuestionSampler,
        answer_strategy_selector: AnswerStrategySelector,
        num_alternatives: int,
        shuffle_answers: bool = True,
        shuffle_questions: bool = True,
        seed: int | None = None
    ):
        self.bank = bank
        self.num_models = num_models
        self.question_sampler = question_sampler
        self.answer_strategy_selector = answer_strategy_selector
        self.num_alternatives = num_alternatives
        self.shuffle_answers = shuffle_answers
        self.shuffle_questions = shuffle_questions
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)

    def build_models(self) -> List[QuizModel]:
        models = []
        for _ in range(self.num_models):
            selected_questions = self.question_sampler.sample(self.bank)
            if self.shuffle_questions:
                random.shuffle(selected_questions)

            quiz_questions: List[QuizQuestion] = []

            for q in selected_questions:
                sampler = self.answer_strategy_selector.select_sampler(q)
                quiz_q = sampler.sample_question(q, self.num_alternatives)

                if self.shuffle_answers and quiz_q.is_shufflable():
                    zipped = list(zip(quiz_q.options, range(len(quiz_q.options))))
                    random.shuffle(zipped)
                    new_options, permutation = zip(*zipped)
                    new_correct = [permutation.index(i) for i in quiz_q.correct_indices]
                    quiz_q = QuizQuestion(
                        statement=quiz_q.statement,
                        options=list(new_options),
                        correct_indices=new_correct,
                        shufflable=quiz_q.shufflable
                    )

                quiz_questions.append(quiz_q)

            models.append(QuizModel(quiz_questions))

        return models

if __name__ == "__main__":
    import os 
    from markdown_question_bank.parser_bank import BankFolderParser
    from markdown_question_bank.sampler_question import CachedQuestionSampler, RandomQuestionSampler
    from markdown_question_bank.sampler_answers import DefaultAnswerStrategySelector
    from markdown_question_bank.quiz_markdown import MarkdownQuizModel
    from markdown_question_bank.sampler_answers import CachedAnswerSampler, DefaultAnswerSampler
    
    folder_path = os.path.join("test_data", "all")
    parser = BankFolderParser(min_wrong=2)
    test_bank = parser.parse(folder_path)

    # A partir do banco de preguntas construimos 2 modelos de cuestionario
    # con 6 preguntas cada un, seleccionando aleatoriamente as preguntas. Ao empregar
    # CachedQuestionSampler, as preguntas seleccionadas son sempre as mesmas en cada
    # modelo. Se se quere que as preguntas sexan diferentes, empregar RandomQuestionSampler
    # en vez de CachedQuestionSampler.
    # Ademais, para cada pregunta seleccionada, seleccionamos aleatoriamente 3 respostas
    # (1 correcta e 2 incorrectas) para cada pregunta. Ao crear cada modelo, pídese a selección
    # de respostas, que tamén será sempre igual ao empregar CachedAnswerSampler(DefaultAnswerSampler()).
    # Deste xeito, teremos 2 modelos coas mesmas preguntas e respostas, coas preguntas na mesma 
    # orde pero  diferentes ordes nas alternativas de cada respostas.

    answer_sampler = CachedAnswerSampler(DefaultAnswerSampler())
    question_sampler = CachedQuestionSampler(RandomQuestionSampler(num_questions=6))

    quiz = QuizBuilder(
        bank=test_bank,
        num_models=2,
        question_sampler=question_sampler,
        answer_strategy_selector=DefaultAnswerStrategySelector(answer_sampler),
        num_alternatives=3,
        shuffle_answers=True,
        shuffle_questions=False,
        seed=2025
    )

    built_models = quiz.build_models()

    markdown_quiz = MarkdownQuizModel(built_models[0])
    markdown_quiz.to_file("0_ES.md", "ES", num_cols=3, with_true_answers=True)
    markdown_quiz.to_file("0_GL.md", "GL", num_cols=3, with_true_answers=True)
    
    markdown_quiz = MarkdownQuizModel(built_models[1])
    markdown_quiz.to_file("1_ES.md", "ES", num_cols=3, with_true_answers=True)
    markdown_quiz.to_file("1_GL.md", "GL", num_cols=3, with_true_answers=True)
