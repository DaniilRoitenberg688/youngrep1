from app.models import Teacher

from app import init_app, db

app = init_app()
app.app_context().push()

for i in Teacher.query.all():
    i.set_schedule({})
    db.session.commit()

