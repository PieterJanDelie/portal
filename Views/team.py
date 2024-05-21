import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, session
from datetime import datetime, timedelta
from services.algemeneFuncties import getRandomImage

team_view = Blueprint('team', __name__, template_folder='templates')

@team_view.route("")
def team():
    # Check if the team content is already in the session and not expired
    if 'team_content' in session:
        expiration_time = session.get('team_expiration')
        if expiration_time and datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
            title_wrap = session['team_content']
            background_source = session.get('background_source', getRandomImage("Sfeer"))
            return render_template("Team/team.html", title_wrap=title_wrap, background_source=background_source)
    
    # If not in session or expired, fetch the data again
    url = "https://bcoostende.be/team/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title_wrap = soup.find("div", class_="bigslam-page-wrapper")

        if title_wrap:
            for a_tag in title_wrap.find_all('a'):
                a_tag.unwrap()
            
            for title in title_wrap.find_all('h3'):
                title.extract()

            # Store the content and the expiration time in the session
            session['team_content'] = str(title_wrap)
            session['team_expiration'] = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            background_source = getRandomImage("Sfeer")
            session['background_source'] = background_source

            return render_template("Team/team.html", title_wrap=title_wrap, background_source=background_source)
        else:
            return "We zijn het team nog aan het samen steken.", 500
    else:
        return "Er liep iets mis.", 500
