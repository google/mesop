import json

from pydantic import BaseModel


class EvalQuestion(BaseModel):
  name: str
  question: str


with open("eval_questions.json") as f:
  eval_questions_str = f.read()

eval_questions = [EvalQuestion(**q) for q in json.loads(eval_questions_str)]
