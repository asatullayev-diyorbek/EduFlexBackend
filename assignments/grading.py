import re
from .models import AssignmentTask, TaskResponse


def auto_grade_response(task: AssignmentTask, response: TaskResponse) -> float | None:
    """
    Returns score (float) if auto-grading is possible, else None.
    """
    if task.task_type == 'short_answer':
        pattern = task.config.get('answer_pattern', '').strip()
        if not pattern:
            return None  # no pattern → manual grade

        flags = 0 if task.config.get('case_sensitive', False) else re.IGNORECASE
        try:
            if re.search(pattern, response.response_text.strip(), flags):
                return float(task.max_score)
            else:
                return 0.0
        except re.error:
            # Invalid regex — fall back to simple equality
            expected = pattern.lower() if not task.config.get('case_sensitive') else pattern
            actual   = response.response_text.strip()
            actual   = actual.lower() if not task.config.get('case_sensitive') else actual
            return float(task.max_score) if expected == actual else 0.0

    if task.task_type == 'code':
        # Sandbox integration will come in a later phase.
        # For now, code tasks are manually graded.
        return None

    if task.task_type == 'file_upload':
        return None  # always manual

    return None


def grade_submission(submission) -> None:
    """
    Auto-grades all task responses in a submission and updates submission score.
    """
    total_score = 0.0
    total_max   = 0.0
    all_auto    = True

    for response in submission.responses.select_related('task').all():
        task  = response.task
        score = auto_grade_response(task, response)
        total_max += task.max_score

        if score is not None:
            response.score      = score
            response.auto_graded = True
            response.save(update_fields=['score', 'auto_graded'])
            total_score += score
        else:
            all_auto = False
            if response.score is not None:
                total_score += response.score

    submission.max_score = total_max
    submission.score     = total_score if (all_auto or any(
        r.score is not None for r in submission.responses.all()
    )) else None
    submission.save(update_fields=['score', 'max_score'])
