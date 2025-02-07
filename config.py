import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'teachers.db')
    UPLOAD_PATH = 'app/static/teachers_images'
    BASE_PASSWORD = os.environ.get('BASE_PASSWORD')
    print(BASE_PASSWORD)