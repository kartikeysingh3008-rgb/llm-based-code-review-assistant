def calculate_score(analysis):
    score = 0

    # Loops
    score += analysis['loops'] * 2

    # Nesting
    score += analysis['max_nesting_depth'] * 3

    # Long functions
    for func in analysis['functions']:
        if func['length'] > 30:
            score += 5

    return score


def classify_score(score):
    if score <= 5:
        return "Good"
    elif score <= 15:
        return "Moderate"
    else:
        return "Poor"