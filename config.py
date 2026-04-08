import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "devops-mini-projet-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "formations.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False