import json
import random
from flask import Blueprint, render_template, request, session

quiz_view = Blueprint('quiz', __name__, template_folder='templates')

def get_random_question():
    with open('Data/QuizVragen.json', 'r') as f:
        vragen = json.load(f)['vragen']
        return random.choice(vragen)

@quiz_view.route("", methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        vraag_data = get_random_question()
        vraag = vraag_data['vraag']
        mogelijke_antwoorden = vraag_data['mogelijke_antwoorden']
        session['current_quiz_question'] = vraag_data
        return render_template("Quiz/quiz.html", vraag=vraag, mogelijke_antwoorden=mogelijke_antwoorden)
    elif request.method == 'POST':
        answer = request.form['answer']
        vraag_data = session.get('current_quiz_question')
        juist_antwoord = vraag_data['juist_antwoord']
        if answer == juist_antwoord:
            return render_template("Quiz/quiz_correct.html")
        else:
            return render_template("Quiz/quiz_incorrect.html")
