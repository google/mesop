from ai.offline_common.eval import EvalOutcome


def truncate(text: str, max_length: int = 30) -> str:
  if len(text) > max_length:
    return text[:max_length] + "..."
  return text


def calculate_eval_score(eval_outcome: EvalOutcome) -> str:
  return f"{eval_outcome.score / (eval_outcome.examples_run * 3) * 100:.0f}%"
