from flask import Blueprint, render_template

uitslagen_view = Blueprint('uitslagen', __name__, template_folder='templates')

@uitslagen_view.route("")
def uitslagen():
    return render_template("uitslagen.html")