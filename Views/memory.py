import random
from flask import Blueprint, render_template, request
import os
import csv
from datetime import datetime, timedelta

memory_view = Blueprint('memory', __name__, template_folder='templates')

def get_image_paths():
    image_paths = []
    static_dir = "static/"
    for root, _, files in os.walk(static_dir):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def get_images(subfolder):
    image_dir = "static/"+ subfolder
    image_files = [f"{subfolder}/{f}" for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
    return image_files

def getRandomImage(subfolder, InParentFolder=True):
    image_dir = "static/"+ subfolder
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
    if image_files:
        url = ""
        if InParentFolder:
            url += "../"
        url += image_dir + "/" + random.choice(image_files)
        return url
    else:
        return "../static/yellowbackground.jpg" # Default

def write_to_csv(filename, data):
    today_date = datetime.now().strftime('%Y-%m-%d')
    if datetime.now().hour < 7:
        today_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    filepath = f'Data/Responses/{today_date}/{filename}'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)


@memory_view.route("/")
def memory_home():
    return render_template("Memory/memory.html", background_source=getRandomImage("memory/startscherm", InParentFolder=False), imagesources=get_image_paths())

@memory_view.route("/Play")
def memory_game():
    image_paths = get_images("memory/spelers")
    random_images = random.sample(image_paths, k=8)
    card_images = random_images * 2
    random.shuffle(card_images)
    return render_template("Memory/memory_game.html", card_images=card_images, background_source=getRandomImage("memory/eindscherm"))

@memory_view.route("/Einde")
def memory_end():
    moves = request.args.get('moves', type=int)
    time = request.args.get('time', type=int)
    write_to_csv("Memory/Eindscores.csv", [datetime.now(), moves, time])
    return render_template("Memory/memory_end.html", num_moves=moves, tijd=time, background_source=getRandomImage("memory/eindscherm"))
