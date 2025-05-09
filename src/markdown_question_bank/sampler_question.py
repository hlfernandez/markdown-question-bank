import random
from abc import ABC, abstractmethod
from typing import List
from markdown_question_bank.bank import Bank
from markdown_question_bank.question import Question

class QuestionSampler(ABC):
    @abstractmethod
    def sample(self, bank: Bank) -> List[Question]:
        pass

class RandomQuestionSampler(QuestionSampler):
    def __init__(self, num_questions: int, seed: int | None = None):
        self.num_questions = num_questions
        self.seed = seed

    def sample(self, bank: Bank) -> List[Question]:
        if self.seed is not None:
            random.seed(self.seed)

        questions = random.sample(bank.get_questions(), self.num_questions)

        return questions

class TopicQuestionSampler(QuestionSampler):
    def __init__(self, topic_counts: dict[str, int], total: int, seed: int | None = None):
        self.topic_counts = topic_counts
        self.total = total
        self.seed = seed

    def sample(self, bank: Bank) -> List[Question]:
        if self.seed is not None:
            random.seed(self.seed)

        selected = []
        used_ids: set[int] = set()

        for topic, n in self.topic_counts.items():
            candidates = bank.get_questions_by_topic(topic)
            sample = random.sample(candidates, min(n, len(candidates)))
            selected.extend(sample)
            used_ids.update(id(q) for q in sample)

        remaining = self.total - len(selected)
        if remaining > 0:
            all_questions = bank.get_questions()
            pool = [q for q in all_questions if id(q) not in used_ids]
            filler = random.sample(pool, min(remaining, len(pool)))
            selected.extend(filler)

        return selected

class CachedQuestionSampler(QuestionSampler):
    def __init__(self, inner_sampler: QuestionSampler):
        self.inner_sampler = inner_sampler
        self._cached: List[Question] | None = None

    def sample(self, bank: Bank) -> List[Question]:
        if self._cached is None:
            self._cached = self.inner_sampler.sample(bank)
        return self._cached
