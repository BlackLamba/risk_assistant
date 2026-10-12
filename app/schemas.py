
from pydantic import BaseModel, Field, model_validator


class ProjectInput(BaseModel):
    total_tasks: int = Field(ge=1, description="Всего задач")
    blocked_tasks: int = Field(ge=0, description="Заблокированные задачи")
    available_developers: int = Field(ge=1, description="Доступные разработчики")
    critical_bugs: int = Field(ge=0, description="Критические ошибки")
    delay_probability: float = Field(
        ge=0, le=1, description="Вероятность задержки от 0 до 1"
    )
    budget_remaining: float = Field(gt=0, description="Оставшийся бюджет")
    estimated_cost_remaining: float = Field(
        gt=0, description="Оценка оставшихся расходов"
    )

    @model_validator(mode="after")
    def validate_blocked_tasks(self):
        if self.blocked_tasks > self.total_tasks:
            raise ValueError(
                "Количество заблокированных задач не может превышать общее число задач"
            )
        return self


class RiskAssessment(BaseModel):
    risk_score: int = Field(ge=0, le=100)
    risk_level: str
    explanations: list[str]
    recommendations: list[str]
