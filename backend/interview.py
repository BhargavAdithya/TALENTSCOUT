# backend/interview.py
from llm import ask_technical_question, evaluate_answer

MAX_QUESTIONS = 5


def initial_difficulty(experience: float) -> float:
    if experience <= 0:
        return 2.0
    if experience <= 2:
        return 2.5
    if experience <= 5:
        return 3.5
    return 4.5


def next_difficulty(current: float, passed: bool) -> float:
    if passed:
        return min(5.0, current + 0.2)
    return max(1.0, current - 0.5)