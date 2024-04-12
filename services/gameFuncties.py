import json
import random
import os
import csv
from datetime import datetime, timedelta

def get_image_paths():
    image_paths = []
    static_dir = "static/"
    for root, _, files in os.walk(static_dir):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def get_random(filename, hoofdvariabele, asked_objecten = [], localvariabele = ""):
    with open('Data/' + filename, 'r') as f:
        hoofdObject = json.load(f)[hoofdvariabele]
        if len(asked_objecten) <= 0:
            return hoofdObject
        else:
            beschikbare_objecten = [obj for obj in hoofdObject if hoofdObject[localvariabele] not in asked_objecten]
            return random.choice(beschikbare_objecten)

def write_to_csv(filename, data):
    today_date = datetime.now().strftime('%Y-%m-%d')
    if datetime.now().hour < 7:
        today_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    filepath = f'Data/Responses/{today_date}/{filename}'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)

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

def get_images(subfolder):
    image_dir = "static/"+ subfolder
    image_files = [f"{subfolder}/{f}" for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
    return image_files