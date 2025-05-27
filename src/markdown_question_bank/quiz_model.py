from typing import List
from dataclasses import dataclass
from markdown_question_bank.question import MultilanguageString, Appendix

@dataclass
class QuizQuestion:
    statement: MultilanguageString
    options: List[MultilanguageString]
    correct_indices: List[int]
    shufflable: bool = True
    appendix: Appendix | None = None

    def is_shufflable(self) -> bool:
        return self.shufflable
    
    def get_appendix(self) -> Appendix | None:
        return self.appendix

@dataclass
class QuizModel:
    questions: List[QuizQuestion]

    def get_questions(self) -> List[QuizQuestion]:
        return self.questions
