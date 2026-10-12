
from app.schemas import ProjectInput, RiskAssessment


def assess_project(project: ProjectInput) -> RiskAssessment:
    score = 0
    explanations: list[str] = []
    recommendations: list[str] = []

    # Доля заблокированных задач: до 30 баллов
    blocked_ratio = project.blocked_tasks / project.total_tasks
    blocked_points = round(blocked_ratio * 30)
    score += blocked_points

    if blocked_ratio >= 0.3:
        explanations.append(
            f"Заблокировано {project.blocked_tasks} из "
            f"{project.total_tasks} задач."
        )
        recommendations.append(
            "Разобрать блокирующие зависимости и назначить ответственных."
        )

    # Критические ошибки: до 20 баллов
    bug_points = min(project.critical_bugs * 5, 20)
    score += bug_points

    if project.critical_bugs > 0:
        explanations.append(
            f"Обнаружено критических ошибок: {project.critical_bugs}."
        )
        recommendations.append(
            "Приоритизировать исправление критических ошибок."
        )

    # Нагрузка команды: до 20 баллов
    tasks_per_developer = (
        project.total_tasks / project.available_developers
    )
    workload_points = min(
        round(max(tasks_per_developer - 5, 0) * 2),
        20,
    )
    score += workload_points

    if workload_points >= 10:
        explanations.append(
            f"Высокая нагрузка: {tasks_per_developer:.1f} задач "
            "на одного разработчика."
        )
        recommendations.append(
            "Пересмотреть объём работ, приоритеты и распределение задач."
        )

    # Вероятность задержки: до 20 баллов
    delay_points = round(project.delay_probability * 20)
    score += delay_points

    if project.delay_probability >= 0.5:
        explanations.append(
            "Высокая экспертная оценка вероятности задержки."
        )
        recommendations.append(
            "Пересчитать сроки с учётом рисков и резервного времени."
        )

    # Давление на бюджет: до 10 баллов
    budget_ratio = (
        project.estimated_cost_remaining / project.budget_remaining
    )
    budget_points = (
        10 if budget_ratio > 1
        else round(budget_ratio * 5)
    )
    score += budget_points

    if budget_ratio > 1:
        explanations.append(
            "Прогноз расходов превышает оставшийся бюджет."
        )
        recommendations.append(
            "Пересмотреть смету, объём работ или доступные ресурсы."
        )

    score = min(score, 100)

    if score < 25:
        level = "low"
    elif score < 50:
        level = "medium"
    elif score < 75:
        level = "high"
    else:
        level = "critical"

    if not explanations:
        explanations.append(
            "По заданным правилам выраженных факторов риска не обнаружено."
        )

    if not recommendations:
        recommendations.append(
            "Продолжать мониторинг сроков, бюджета и блокирующих задач."
        )

    return RiskAssessment(
        risk_score=score,
        risk_level=level,
        explanations=explanations,
        recommendations=recommendations,
    )
