from flask import Blueprint, render_template, request

randanimatie_view = Blueprint('randanimatie', __name__, template_folder='templates')

@randanimatie_view.route("", methods=['GET', 'POST'])
def randanimatie():
    if request.method == 'GET':
        return render_template("randanimatie.html")
    elif request.method == 'POST':
        score = request.form['score']
        return render_template("randanimatie_feedback.html", score=score)