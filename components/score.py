import math

from config import game


def clamp(value):
    """
    The function clamps a value between 0 and 1.
    """
    return min(max(value, 0), 1)


def get_score(total_mistakes, max_mistakes, total_time, max_time):
    """
    The function calculates a score based on the number of mistakes and
    the time taken.

    The score is determined by combining the contributions of mistakes
    and time, normalizing them, and scaling the result to a range from 0
    to 1000.
    """
    mistakes_contribution = clamp(total_mistakes / max_mistakes)
    time_contribution = clamp(total_time / max_time)
    total_contribution = (mistakes_contribution + time_contribution) / 2
    score = math.floor((1 - total_contribution) * 1000)

    return int(score)


def get_score_and_tier(total_mistakes, total_time):
    """
    The function calculates the score and tier based on performance metrics.

    The tier is determined by the calculated score, and can range from 1
    to 3 stars, depending on predefined cutoff values.
    """
    score = get_score(total_mistakes, game.TOTAL_QUESTIONS, total_time,
                      game.MAX_TIME)
    tier = 3

    if score < game.SCORE_1_STAR_CUTOFF:
        tier = 1
    elif score < game.SCORE_2_STAR_CUTOFF:
        tier = 2

    return score, tier
