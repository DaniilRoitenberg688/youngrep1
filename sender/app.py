from fastapi import FastAPI
from aiogram import Bot
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
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
    teacher_id: str = Field(alias='teacherId')
    teacher_name: str = Field(alias='teacherName')
    lesson_date: str = Field(alias='lessonDate')
    lesson_time: str = Field(alias='lessonTime')
    telegram_username: str = Field(alias='telegramUsername')
    phone_number: str = Field(alias='phoneNumber')

@app.post('/api/send_not')
async def send_not(note: Note):
    await bot.send_message(
        chat_id=CHAT_ID, 
        text = f'''
        Новая заявка на пробное занятие
ТГ: {note.telegram_username}
Номер телефона: +{note.phone_number}
ФИО ученика: {note.student_name}
ФИО препода: {note.teacher_name}
Время пробного занятия: {note.lesson_time}
Дата пробного занятия: {note.lesson_date}
        '''
    )
    return {"status": "ok"}
