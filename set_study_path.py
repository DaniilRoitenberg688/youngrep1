from app.models import StudyPath, Teacher

from app import init_app, db

app = init_app()
app.app_context().push()

i: Teacher
for i in Teacher.query.all():
    if i.study_path == StudyPath.all:
        i.study_path = StudyPath.school

db.session.commit()
     
