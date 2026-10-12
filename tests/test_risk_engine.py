
import pytest
from pydantic import ValidationError

from app.schemas import ProjectInput
from app.risk_engine import assess_project


def make_project(**overrides):
    data = {
        "total_tasks": 10,
        "blocked_tasks": 0,
        "available_developers": 3,
        "critical_bugs": 0,
        "delay_probability": 0.1,
        "budget_remaining": 100_000,
        "estimated_cost_remaining": 50_000,
    }
    data.update(overrides)
    return ProjectInput(**data)


def test_low_risk_project():
    result = assess_project(make_project())

    assert result.risk_level == "low"
    assert 0 <= result.risk_score <= 100


def test_critical_project_has_high_risk():
    project = make_project(
        blocked_tasks=8,
        critical_bugs=5,
        available_developers=1,
        delay_probability=0.95,
        budget_remaining=10_000,
        estimated_cost_remaining=20_000,
    )

    result = assess_project(project)

    assert result.risk_level == "critical"
    assert result.risk_score >= 75
    assert result.recommendations


def test_blocked_tasks_cannot_exceed_total():
    with pytest.raises(ValidationError):
        make_project(total_tasks=5, blocked_tasks=6)


def test_score_is_bounded():
    result = assess_project(
        make_project(
            blocked_tasks=10,
            critical_bugs=100,
            delay_probability=1,
            estimated_cost_remaining=200_000,
            budget_remaining=10_000,
        )
    )

    assert 0 <= result.risk_score <= 100


def test_blocked_tasks_increase_risk():
    baseline = assess_project(make_project())
    risky = assess_project(make_project(blocked_tasks=8))

    assert risky.risk_score > baseline.risk_score
