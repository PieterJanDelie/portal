import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template

team_view = Blueprint('team', __name__, template_folder='templates')

@team_view.route("")
def team():
    url = "https://bcoostende.be/team/"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        title_wrap = soup.find("div", class_="bigslam-page-title-wrap bigslam-style-custom bigslam-center-align")
        page_wrapper = soup.find("div", class_="bigslam-page-wrapper")

        if title_wrap and page_wrapper:
            for a_tag in page_wrapper.find_all('a'):
                a_tag.decompose()

            title_wrap_style = title_wrap.get("style")

            return render_template("Team/team.html", title_wrap=title_wrap, page_wrapper=page_wrapper,
                                   title_wrap_style=title_wrap_style)
        else:
            return "We zijn het team nog aan het samen steken.", 500
    else:
        return "Er liep iets mis.", 500
