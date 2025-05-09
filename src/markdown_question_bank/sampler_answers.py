import random
from abc import ABC, abstractmethod
from typing import List
from markdown_question_bank.question import Question, MultilanguageString
from markdown_question_bank.quiz_model import QuizQuestion

class AnswerSampler(ABC):
    @abstractmethod
    def sample_question(self, question: Question, num_alternatives: int) -> QuizQuestion:
        pass

class DefaultAnswerSampler(AnswerSampler):
    def sample_question(self, question: Question, num_alternatives: int) -> QuizQuestion:
        correct = question.get_right_answers()
        wrong = question.get_wrong_answers()

        # Eliximos unha resposta correcta ao azar
        correct_choice = random.choice(correct)

        # Seleccionamos (num_alternatives - 1) incorrectas
        num_wrong = num_alternatives - 1
        wrong_choices = random.sample(wrong, min(num_wrong, len(wrong)))

        options: List[MultilanguageString] = [correct_choice] + wrong_choices
        random.shuffle(options)

        correct_indices = [i for i, o in enumerate(options) if o == correct_choice]
        return QuizQuestion(
            statement=question.get_statement(),
            options=options,
            correct_indices=correct_indices,
            shufflable=True  # As opcións por defecto son barallables
        )

class CachedAnswerSampler(AnswerSampler):
    def __init__(self, sampler: AnswerSampler):
        self.sampler = sampler
        self.cache = {}

    def sample_question(self, question: Question, num_alternatives: int) -> QuizQuestion:
        cache_key = (id(question), num_alternatives)
        if cache_key not in self.cache:
            self.cache[cache_key] = self.sampler.sample_question(question, num_alternatives)
        return self.cache[cache_key]

class AnswerStrategySelector(ABC):
    @abstractmethod
    def select_sampler(self, question: Question) -> AnswerSampler:
        pass

class DefaultAnswerStrategySelector(AnswerStrategySelector):
    def __init__(self):
        self.default_sampler = CachedAnswerSampler(DefaultAnswerSampler())

    def select_sampler(self, question: Question) -> AnswerSampler:
        return self.default_sampler
