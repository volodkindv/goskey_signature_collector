from ..database.models import AppealModel


def format_appeal(appeal: AppealModel) -> str:
    return f"/appeals_{appeal.id} {appeal.text} [{appeal.file_name}]"


def format_appeal_admin(appeal: AppealModel) -> str:
    mark = "[скрыта]" if appeal.is_hidden else ""
    return f"/admin_appeals_{appeal.id} {mark} {appeal.text} [{appeal.file_name}]"
