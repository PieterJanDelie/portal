import json
import random
from flask import Blueprint, render_template, request, session

quiz_view = Blueprint('quiz', __name__, template_folder='templates')

def get_random_question():
    with open('Data/QuizVragen.json', 'r') as f:
        vragen = json.load(f)['vragen']
        return random.choice(vragen)

@quiz_view.route("/")
def quiz_home():
    session['questions_answered'] = 0
    session['correct_answers'] = 0
    return render_template("Quiz/quiz.html")

@quiz_view.route("/StartQuiz", methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'GET':
        if session.get('questions_answered', 0) >= 5:
            eindscore = session.get('correct_answers', 0)
            session.pop('questions_answered', None)
            session.pop('correct_answers', None)
            return render_template("Quiz/quiz_end.html", eindscore=eindscore)
        else:
            vraag_data = get_random_question()
            vraag = vraag_data['vraag']
            mogelijke_antwoorden = vraag_data['mogelijke_antwoorden']
            session['current_quiz_question'] = vraag_data
            return render_template("Quiz/quiz_start.html", vraag=vraag, mogelijke_antwoorden=mogelijke_antwoorden)
    elif request.method == 'POST':
        session['questions_answered'] += 1
        vraag_data = session.get('current_quiz_question')
        juist_antwoord = vraag_data['juist_antwoord']
        answer = request.form['answer']
        if answer == juist_antwoord:
            session['correct_answers'] = session.get('correct_answers', 0) + 1

        if session['questions_answered'] >= 5:
            eindscore = session.get('correct_answers', 0)
            session.pop('questions_answered', None)
            session.pop('correct_answers', None)
            return render_template("Quiz/quiz_end.html", eindscore=eindscore)

        if answer == juist_antwoord:
            return render_template("Quiz/quiz_correct.html", antwoord=juist_antwoord, laatste_tekstje=vraag_data["laatste_tekstje"])
        else:
            return render_template("Quiz/quiz_incorrect.html", antwoord=juist_antwoord, geantwoord=answer, laatste_tekstje=vraag_data["laatste_tekstje"])
