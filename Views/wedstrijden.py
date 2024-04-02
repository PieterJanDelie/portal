from flask import Blueprint, render_template

wedstrijden_view = Blueprint('wedstrijden', __name__, template_folder='templates')

@wedstrijden_view.route("")
def wedstrijden():
    return render_template("wedstrijden.html")