import math
from config import game


def clamp(value):
    return min(max(value, 0), 1)


def get_score(total_miskates, max_mistakes, total_time, max_time):
    mistakes_contribution = clamp(total_miskates / max_mistakes)
    time_contribution = clamp(total_time / max_time)
    total_contribution = (mistakes_contribution + time_contribution) / 2
    score = math.floor((1 - total_contribution) * 1000)

    return int(score)


def get_score_and_tier(total_miskates, total_time):
    score = get_score(total_miskates, game.TOTAL_QUESTIONS, total_time,
                      game.MAX_TIME)
    tier = 3

    if score < game.SCORE_1_STAR_CUTOFF:
        tier = 1
    elif score < game.SCORE_2_STAR_CUTOFF:
        tier = 2

    return score, tier
