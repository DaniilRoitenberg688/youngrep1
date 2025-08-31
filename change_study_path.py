from app import init_app
from app import db
from app.models import Teacher, User, StudyPath


app = init_app()
app.app_context().push()


i: Teacher
for i in Teacher.query.all():
    if i.study_path == StudyPath.oge:
        i.is_oge = True
    elif i.study_path == StudyPath.school:
        i.is_school = True
    elif i.study_path == StudyPath.olymps:
        i.is_olymps = True

db.session.commit()
    
