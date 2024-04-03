from flask import Blueprint

def register_blueprints(app):
    home = Blueprint('home', __name__, template_folder='templates')
    kalender = Blueprint('kalender', __name__, template_folder='templates')
    wedstrijden = Blueprint('wedstrijden', __name__, template_folder='templates')
    uitslagen = Blueprint('uitslagen', __name__, template_folder='templates')
    team = Blueprint('team', __name__, template_folder='templates')
    quiz = Blueprint('quiz', __name__, template_folder='templates')
    randanimatie = Blueprint('randanimatie', __name__, template_folder='templates')
    feedback = Blueprint('feedback', __name__, template_folder='templates')

    from .home import home_view
    from .kalender import kalender_view
    from .stand import stand_view
    from .uitslagen import uitslagen_view
    from .team import team_view
    from .quiz import quiz_view
    from .feedback import feedback_view

    app.register_blueprint(home)
    app.register_blueprint(kalender)
    app.register_blueprint(wedstrijden)
    app.register_blueprint(uitslagen)
    app.register_blueprint(team)
    app.register_blueprint(quiz)
    app.register_blueprint(randanimatie)
    app.register_blueprint(feedback)

    app.add_url_rule("/", view_func=home_view)
    app.add_url_rule("/Kalender", view_func=kalender_view)
    app.add_url_rule("/Stand", view_func=stand_view)
    app.add_url_rule("/Uitslagen", view_func=uitslagen_view)
    app.add_url_rule("/Team", view_func=team_view)
    app.add_url_rule("/Quiz", view_func=quiz_view)
    app.add_url_rule("/Feedback", view_func=feedback_view)