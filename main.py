from flask import Flask, redirect, url_for
from Views.home import home
from Views.kalender import kalender
from Views.stand import stand
from Views.uitslagen import uitslagen
from Views.team import team
from Views.quiz import start_quiz
from Views.quiz import quiz_home
from Views.feedback import feedback
from Views.memory import memory_home, memory_game, memory_end

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.add_url_rule("/", view_func=home)
app.add_url_rule("/Kalender", view_func=kalender)
app.add_url_rule("/Stand", view_func=stand)
app.add_url_rule("/Uitslagen", view_func=uitslagen)
app.add_url_rule("/Team", view_func=team)
app.add_url_rule("/Quiz", view_func=quiz_home)
app.add_url_rule("/Quiz/StartQuiz", view_func=start_quiz, methods=['GET', 'POST'])
app.add_url_rule("/Feedback", view_func=feedback, methods=['GET', 'POST'])
app.add_url_rule("/Memory", view_func=memory_home)
app.add_url_rule("/Memory/Play", view_func=memory_game)
app.add_url_rule("/Memory/Einde", view_func=memory_end)


@app.errorhandler(Exception)
def handle_exception(e):
    return redirect(url_for('quiz.quiz_home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT'))