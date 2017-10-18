from flask import Flask

mainApp = Flask(__name__)
mainApp.config.from_object('config')

from app import views