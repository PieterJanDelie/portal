from flask import Blueprint, render_template, request

feedback_view = Blueprint('feedback', __name__, template_folder='templates')

@feedback_view.route("", methods=['GET', 'POST'])
def feedback():
    if request.method == 'GET':
        return render_template("feedback.html")
    elif request.method == 'POST':
        feedback = request.form['feedback']
        return render_template("feedback_thanks.html", feedback=feedback)