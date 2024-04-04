import json
import random
from flask import Blueprint, render_template, request, session, redirect, url_for

quiz_view = Blueprint('quiz', __name__, template_folder='templates')

def get_random_question():
    with open('Data/QuizVragen.json', 'r') as f:
        vragen = json.load(f)['vragen']
        return random.choice(vragen)
    
@quiz_view.route("/")
def quiz_home():
    session['questions_answered'] = 0  # Reset het aantal beantwoorde vragen
    return render_template("Quiz/quiz.html")

@quiz_view.route("/StartQuiz", methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'GET':
        if session.get('questions_answered', 0) >= 5:
            return redirect(url_for('quiz_home'))
        else:
            vraag_data = get_random_question()
            vraag = vraag_data['vraag']
            mogelijke_antwoorden = vraag_data['mogelijke_antwoorden']
            session['current_quiz_question'] = vraag_data
            return render_template("Quiz/quiz_start.html", vraag=vraag, mogelijke_antwoorden=mogelijke_antwoorden)
    elif request.method == 'POST':
        session['questions_answered'] += 1
        if session['questions_answered'] >= 5:
            return redirect(url_for('quiz_home'))
        
        answer = request.form['answer']
        vraag_data = session.get('current_quiz_question')
        juist_antwoord = vraag_data['juist_antwoord']
        if answer == juist_antwoord:
            return render_template("Quiz/quiz_correct.html")
        else:
            return render_template("Quiz/quiz_incorrect.html")
