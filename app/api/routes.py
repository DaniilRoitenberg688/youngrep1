from app.api import bp
from app.models import Teacher, Subject

@bp.route("/teachers")
def get_all_teachers():
    all_teachers: list[Teacher] = Teacher.query.all()
    return [{
        "id": teacher.id,
        "name": f"{teacher.surname} {teacher.name}" 
    } for teacher in all_teachers]


@bp.route("/subjects")
def get_subjects():
    res = Subject.query.all()
    return [{
        "id": s.id,
        "name": f"{s.name}" 
    } for s in res]



