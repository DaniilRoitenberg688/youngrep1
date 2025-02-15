from app import init_app, db
from app.models import Teacher

app = init_app()
with app.app_context():
    teachers: list[Teacher] = Teacher.query.all()
    for i in range(len(teachers)):
        teachers[i].position = teachers[i].id

    db.session.commit()