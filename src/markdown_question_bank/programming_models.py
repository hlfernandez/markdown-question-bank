import json

class ProgrammingQuestionInfo:
    def __init__(self, dir: str, score: str):
        self.dir = dir
        self.score = score

    def __repr__(self):
        return f"ProgrammingQuestionInfo(dir={self.dir}, score={self.score})"

class ProgrammingModel:
    def __init__(self, questions: list[ProgrammingQuestionInfo]):
        self.questions = questions  # list of ProgrammingQuestionInfo, index+1 is the question number

    def count(self) -> int:
        return len(self.questions)

    def get(self, number: str) -> ProgrammingQuestionInfo:
        idx = int(number) - 1
        return self.questions[idx]

    def __repr__(self):
        return f"ProgrammingModel(questions={self.questions})"

class ProgrammingModels:
    def __init__(self, models: list[ProgrammingModel]):
        self.models = models

    @staticmethod
    def from_json(json_path: str) -> 'ProgrammingModels':
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        models_list = []
        for model_dict in data["models:"]:
            questions = []
            for info in model_dict["problems"]:
                questions.append(ProgrammingQuestionInfo(
                    dir=info["dir"],
                    score=info["score"]
                ))
            models_list.append(ProgrammingModel(questions))
        return ProgrammingModels(models_list)

    def __getitem__(self, idx) -> ProgrammingModel:
        return self.models[idx]

    def __len__(self):
        return len(self.models)
