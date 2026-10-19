from apps.studies.models import StudyMilestone, StudyObjective
from apps.visits.models import VisitDefinition


def apply_template(study, template, user):
    for index, item in enumerate(template.default_milestones or []):
        StudyMilestone.objects.get_or_create(
            organization=study.organization,
            study=study,
            name=item.get("name", f"Milestone {index + 1}"),
            defaults={"sequence": index, "created_by": user},
        )
    for index, item in enumerate(template.default_objectives or []):
        StudyObjective.objects.get_or_create(
            organization=study.organization,
            study=study,
            text=item.get("text", ""),
            defaults={"kind": item.get("kind", "primary"), "sequence": index, "created_by": user},
        )
    for index, item in enumerate(template.default_visits or []):
        VisitDefinition.objects.get_or_create(
            organization=study.organization,
            study=study,
            code=item.get("code", f"V{index + 1}"),
            defaults={
                "name": item.get("name", f"Visit {index + 1}"),
                "sequence": index,
                "window_start_days": item.get("window_start_days", -3),
                "window_end_days": item.get("window_end_days", 3),
                "created_by": user,
            },
        )
    if template.phase:
        study.phase = template.phase
    if template.therapeutic_area:
        study.therapeutic_area = template.therapeutic_area
    study.save()
    return study
