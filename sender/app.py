from fastapi import FastAPI
from aiogram import Bot
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
import os


load_dotenv()

CHAT_ID = os.environ.get('CHAT_ID') or ''
TOKEN = os.environ.get('TOKEN') or ''

app = FastAPI()
bot = Bot(token=TOKEN)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Note(BaseModel):
    student_name: str = Field(alias='studentName')
    teacher_id: str = Field(alias='subjectId')
    teacher_name: str = Field(alias='subjectName')
    lerning_request: str = Field(alias='learningRequest')
    telegram_username: str = Field(alias='telegramUsername')
    phone_number: str = Field(alias='phoneNumber')
    contact_methods: list[str] = Field(alias='contactMethods')
    
    @field_validator('telegram_username', mode='before')
    @classmethod
    def set_dog(cls, value: str) -> str:
        if value[0] == '@':
            return value
        return '@' + value



@app.post('/api/send_not')
async def send_not(note: Note):
    await bot.send_message(
        chat_id=CHAT_ID, 
        text = f'''
        Новая заявка на пробное занятие
ТГ: {note.telegram_username}
Номер телефона: +{note.phone_number}
Как обращаться: {note.student_name}
ФИО препода: {note.teacher_name}
Способы связи: {', '.join(note.contact_methods)}
Проблемы: {note.lerning_request}
        '''
    )
    return {"status": "ok"}





class TeacherNote(BaseModel):
    student_name: str = Field(alias='studentName')
    teacher_id: str = Field(alias='teacherId')
    teacher_name: str = Field(alias='teacherName')
    telegram_username: str = Field(alias='telegramUsername')
    phone_number: str = Field(alias='phoneNumber')
    contact_methods: list[str] = Field(alias='contactMethods')
    
    @field_validator('telegram_username', mode='before')
    @classmethod
    def set_dog(cls, value: str) -> str:
        if value[0] == '@':
            return value
        return '@' + value



@app.post('/api/send_teacher_not')
async def send_teacher_not(note: TeacherNote):
    await bot.send_message(
        chat_id=CHAT_ID, 
        text = f'''
Новая заявка на преподавание
ТГ: {note.telegram_username}
Номер телефона: +{note.phone_number}
ФИО: {note.student_name}
Предмет: {note.teacher_name}
Способы связи: {', '.join(note.contact_methods)}
        '''
    )
    return {"status": "ok"}
