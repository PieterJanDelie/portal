import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template
from services.algemeneFuncties import getRandomImage

team_view = Blueprint('team', __name__, template_folder='templates')

@team_view.route("")
def team():
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


            background_source = background_source=getRandomImage("Sfeer")
            return render_template("Team/team.html", title_wrap=title_wrap, background_source = background_source)
        else:
            return "We zijn het team nog aan het samen steken.", 500
    else:
        return "Er liep iets mis.", 500
