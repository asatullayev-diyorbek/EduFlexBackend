"""Grading logic for each question type."""


def grade_answer(question, user_answer) -> tuple[bool, float]:
    """Return (is_correct, points_earned)."""
    q_type = question.type
    data = question.data
    points = question.points

    if q_type == 'poll':
        return True, points

    if user_answer is None:
        return False, 0

    if q_type == 'multiple_choice':
        correct = data.get('correct')
        # correct can be a single value or list (multi-select)
        if isinstance(correct, list):
            user_list = user_answer if isinstance(user_answer, list) else [user_answer]
            is_correct = sorted(str(x) for x in user_list) == sorted(str(x) for x in correct)
        else:
            is_correct = str(user_answer) == str(correct)
        return is_correct, points if is_correct else 0

    if q_type == 'true_false':
        correct = data.get('correct')
        is_correct = str(user_answer).lower() == str(correct).lower()
        return is_correct, points if is_correct else 0

    if q_type == 'fill_blank':
        answers = data.get('answers', {})
        if not isinstance(user_answer, dict):
            return False, 0
        total_blanks = len(answers)
        if total_blanks == 0:
            return True, points
        correct_count = 0
        for key, expected in answers.items():
            user_val = user_answer.get(key, '')
            if str(user_val).strip().lower() == str(expected).strip().lower():
                correct_count += 1
        ratio = correct_count / total_blanks
        earned = round(points * ratio, 2)
        return ratio == 1.0, earned

    if q_type == 'matching':
        pairs = data.get('pairs', {})
        if not isinstance(user_answer, dict) or not pairs:
            return False, 0
        total = len(pairs)
        correct_count = sum(
            1 for k, v in pairs.items()
            if str(user_answer.get(k, '')).strip().lower() == str(v).strip().lower()
        )
        ratio = correct_count / total
        earned = round(points * ratio, 2)
        return ratio == 1.0, earned

    if q_type == 'ordering':
        correct_order = data.get('correct_order', [])
        if not isinstance(user_answer, list) or not correct_order:
            return False, 0
        is_correct = [str(x) for x in user_answer] == [str(x) for x in correct_order]
        return is_correct, points if is_correct else 0

    return False, 0
