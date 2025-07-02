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

    @staticmethod
    def from_bank(bank: Bank, total: int, seed: int | None = None) -> 'TopicQuestionSampler':
        topics = bank.get_topics()

        if not topics:
            raise ValueError("No topics found in the bank.")

        n_topics = len(topics)
        per_topic = total // n_topics
        remainder = total % n_topics
        topic_counts = {topic: per_topic for topic in topics}
        for topic in list(topics)[:remainder]:
            topic_counts[topic] += 1

        return TopicQuestionSampler(topic_counts, total, seed)

class CachedQuestionSampler(QuestionSampler):
    def __init__(self, inner_sampler: QuestionSampler):
        self.inner_sampler = inner_sampler
        self._cached: List[Question] | None = None

    def sample(self, bank: Bank) -> List[Question]:
        if self._cached is None:
            self._cached = self.inner_sampler.sample(bank)
        return self._cached
