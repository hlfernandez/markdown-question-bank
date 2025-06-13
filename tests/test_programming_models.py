from markdown_question_bank.programming_models import ProgrammingModels, ProgrammingModel, ProgrammingQuestionInfo

def test_programming_models_from_json():
    models = ProgrammingModels.from_json('test_data/programming/models.json')
    assert len(models) == 2
    model1 = models[0]
    model2 = models[1]
    assert isinstance(model1, ProgrammingModel)
    assert model1.count() == 2
    q1 = model1.get("1")
    assert isinstance(q1, ProgrammingQuestionInfo)
    assert q1.dir == "lists_1"
    assert q1.score == "5"
    q2 = model2.get("2")
    assert q2.dir == "strings_2"
