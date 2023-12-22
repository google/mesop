import logging
import time
from typing import Callable


def exponential_backoff(
  predicate_fn: Callable[[], bool],
  *,
  max_attempts: int = 5,
  initial_delay: float = 1.0,
  backoff_factor: float = 3,
):
  delay = initial_delay
  for attempt in range(max_attempts):
    if predicate_fn():
      break
    else:
      logging.info(
        f"Attempt {attempt+1} failed, retrying in {delay} seconds...",
      )
      time.sleep(delay)
      delay *= backoff_factor
  else:
    logging.error("Max attempts reached, operation failed.")
