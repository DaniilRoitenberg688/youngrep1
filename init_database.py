from app import db, init_app
from app.models import Achievement, Hobby, Subject

app = init_app()

all_subjects = ["Математика", "Программирование", "Физика", "Химия", "Биология"]
all_achievements = [
    "победитель_ВСОШ",
    "призер_ВСОШ",
    "победитель_перечневой_олимпиады_1_уровня",
    "призер_перечневой_олимпиады_1_уровня",
    "другие...",
]
all_hobbies = [
    "Спорт",
    "Творчество",
    "Литература",
    "Научные_исследования",
    "Компьютерные_игры",
    "Настольные_игры",
    "другие...",
]

with app.app_context():
    for i in all_subjects:
        s = Subject(name=i)
        db.session.add(s)

    for i in all_achievements:
        s = Achievement(name=i)
        db.session.add(s)

    for i in all_hobbies:
        s = Hobby(name=i)
        db.session.add(s)

    db.session.commit()
