import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from analytics import performance_score, trend_status, intervention_status

def test_performance_score():
    assert performance_score(80, 80, 80, 80) == 80

def test_declining_trend():
    assert trend_status(75, 64) == "Declining"

def test_improving_trend():
    assert trend_status(60, 72) == "Improving"

def test_stable_trend():
    assert trend_status(70, 75) == "Stable"

def test_low_attendance_triggers_intervention():
    status, reasons = intervention_status(70, 60, "Stable")
    assert status == "Needs Intervention"
    assert "Low attendance" in reasons

def test_invalid_score_inputs_rejected():
    with pytest.raises(ValueError):
        performance_score(110, 80, 80, 80)


@pytest.mark.parametrize(
    ('previous', 'latest', 'expected'),
    [(4.08, 14.08, 'Improving'), (14.08, 4.08, 'Declining'), (4.08, 14.07, 'Stable')],
)
def test_decimal_scores_at_trend_threshold(previous, latest, expected):
    assert trend_status(previous, latest) == expected
