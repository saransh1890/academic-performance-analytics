import math


def performance_score(exam_avg, assignment_avg, attendance_pct, internal_avg):
    """Weighted score, assuming each input is on a 0-100 scale."""
    values = [exam_avg, assignment_avg, attendance_pct, internal_avg]
    if any(not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0 or v > 100 for v in values):
        raise ValueError("All indicators must be between 0 and 100")
    return round(0.40 * exam_avg + 0.25 * assignment_avg +
                 0.20 * attendance_pct + 0.15 * internal_avg, 2)

def trend_status(previous_score, latest_score, threshold=10):
    if previous_score is None:
        return "No Previous Data"
    delta = latest_score - previous_score
    if delta <= -threshold:
        return "Declining"
    if delta >= threshold:
        return "Improving"
    return "Stable"

def intervention_status(score, attendance_pct, trend):
    reasons = []
    if score < 50:
        reasons.append("Low performance score")
    if attendance_pct < 75:
        reasons.append("Low attendance")
    if trend == "Declining":
        reasons.append("Declining performance")
    return ("Needs Intervention" if reasons else "Normal", reasons)
