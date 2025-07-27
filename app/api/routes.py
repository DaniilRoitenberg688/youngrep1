from app.api import bp
from app.models import Teacher

@bp.route("/teachers")
def get_all_teachers():
    all_teachers: list[Teacher] = Teacher.query.all()
    return [{
        "id": teacher.id,
        "name": f"{teacher.surname} {teacher.name}" 
    } for teacher in all_teachers]


