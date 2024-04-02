from flask import Blueprint, render_template, request

quiz_view = Blueprint('quiz', __name__, template_folder='templates')

@quiz_view.route("", methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        return render_template("quiz.html")
    elif request.method == 'POST':
        answer = request.form['answer']
        if answer == 'c':
            return render_template("quiz_correct.html")
        else:
            return render_template("quiz_incorrect.html")