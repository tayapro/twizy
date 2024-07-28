from config import game

def calculate_quiz_score(correct_answers, time_taken):
    # base_score = 100
    # max_time = 600
    # time_bonus_factor = 5

    # Calculate correct answers score
    correct_score = correct_answers * base_score
    
    # Calculate time bonus
    time_bonus = max(0, (max_time - time_taken) * time_bonus_factor)
    
    # Calculate final score
    final_score = correct_score + time_bonus
    
    # Normalize final score, 1000 points is max
    max_possible_score = total_questions * base_score + max_time * time_bonus_factor
    normalized_score = (final_score / max_possible_score) * 1000
    normalized_score = min(max(0, normalized_score), 1000)
    
    return round(normalized_score)