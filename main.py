from flask import Flask, request, render_template
from config import Config
from Views.home import home
from Views.kalender import kalender
from Views.wedstrijden import wedstrijden
from Views.uitslagen import uitslagen
from Views.team import team
from Views.quiz import quiz
from Views.randanimatie import randanimatie
from Views.feedback import feedback

app = Flask(__name__)
app.config.from_object(Config)

app.add_url_rule("/", view_func=home)
app.add_url_rule("/Kalender", view_func=kalender)
app.add_url_rule("/Wedstrijden", view_func=wedstrijden)
app.add_url_rule("/Uitslagen", view_func=uitslagen)
app.add_url_rule("/Team", view_func=team)
app.add_url_rule("/quiz", view_func=quiz)
app.add_url_rule("/randanimatie", view_func=randanimatie)
app.add_url_rule("/feedback", view_func=feedback)

if __name__ == "__main__":
    app.run()