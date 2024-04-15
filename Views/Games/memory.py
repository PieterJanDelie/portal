import random
from flask import Blueprint, render_template, request
from datetime import datetime
from services.gameFuncties import get_images, getRandomImage, write_to_csv

memory_view = Blueprint('memory', __name__, template_folder='templates')

@memory_view.route("/")
def memory_home():
    return render_template("Games/Memory/memory.html", background_source=getRandomImage("Games/Memory/Startscherm", InParentFolder=False))

@memory_view.route("/Play")
def memory_game():
    image_paths = get_images("Games/Memory/Spelers")
    random_images = random.sample(image_paths, k=8)
    card_images = random_images * 2
    random.shuffle(card_images)
    return render_template("Games/Memory/memory_game.html", card_images=card_images, background_source=getRandomImage("Games/Memory/Eindscherm"))

@memory_view.route("/Einde")
def memory_end():
    moves = request.args.get('moves', type=int)
    time = request.args.get('time', type=int)
    write_to_csv("Memory/Eindscores.csv", [datetime.now(), moves, time])
    return render_template("Games/Memory/memory_end.html", num_moves=moves, tijd=time, background_source=getRandomImage("Games/Memory/Eindscherm"))
