from flask import Flask, request, render_template, session
from config import Config
from Views.home import home
from Views.kalender import kalender
from Views.stand import stand
from Views.uitslagen import uitslagen
from Views.team import team
from Views.quiz import quiz
from Views.feedback import feedback

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
app.config.from_object(Config)

app.add_url_rule("/", view_func=home)
app.add_url_rule("/Kalender", view_func=kalender)
app.add_url_rule("/Stand", view_func=stand)
app.add_url_rule("/Uitslagen", view_func=uitslagen)
app.add_url_rule("/Team", view_func=team)
app.add_url_rule("/Quiz", view_func=quiz, methods=['GET', 'POST'])
app.add_url_rule("/Feedback", view_func=feedback, methods=['GET', 'POST'])


if __name__ == "__main__":
    app.run()