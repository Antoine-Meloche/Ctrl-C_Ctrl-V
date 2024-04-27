import csv
#import datetime
from datetime import date, datetime, timedelta
from enum import Enum
import math
import exiftool
from ultralytics import YOLO
import requests
from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import JSONResponse
import aiofiles
import os
import random
import string
import pickle

def main():
    """
    The hierarchy in csv is of a constant value
    The size is of a higher ordernance(determined by big,medium,small)
    The time of day : increase in times of no traffic in roads but also increase according to the hierarchy size.
    """
    with open("VOIE_PUBLIQUE.csv", newline='', encoding="utf-8") as csvfile:
        typelist = []
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader: 
            #print(row[17])
            if row[17] not in typelist:
                typelist.append(row[17])
                
            
            #input()
            
        #print(typelist)


    Pothole("Rue de la Coopération", 27337.65215505029, -75.7398916666667, 45.421775).add_pothole_to_list()
    Pothole("Rue de la Coopération", 27337.65215505029, -75.7398916666667, 45.421775, datetime.now()-timedelta(days=1)).add_pothole_to_list()
    Pothole("Rue de la Coopération", 46764.74977358413, -75.7411416666667, 45.4219527777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 45392.76963265286, -75.7411416666667, 45.4219527777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 82539.61783350975, -75.7411416666667, 45.4219527777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 8178.726142000768, -75.7411416666667, 45.4219527777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 4939.061254910656, -75.7411416666667, 45.4219527777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 3738.7151497133636, -75.7411416666667, 45.4219527777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 1153583.3721435706, -75.7411416666667, 45.4219527777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 69567.92688925816, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 370368.8547083, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 4867.301275874248, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 65178.743932303616, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 100729.14818992285, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 15835.160141739367, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 25937.27854529452, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 120979.37786848977, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Boulevard de Lucerne", 29136.329548451795, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 18841.292545498713, -75.7400027777778, 45.4226527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 105835.160141739367, -75.7406833333333, 45.4243027777778, datetime.now()-timedelta(days=1)).add_pothole_to_list()
    Pothole("Chemin d'Aylmer", 183937.27854529452, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue du Roussillon", 120979.37786848977, -75.7406833333333, 45.4243027777778, datetime.now()-timedelta(days=7)).add_pothole_to_list()
    Pothole("Rue Victor-Beaudry", 29136.329548451795, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 18841.292545498713, -75.7400027777778, 45.4226527777778, datetime.now()-timedelta(days=31)).add_pothole_to_list()
    print("Potholes:")
    for pothole in Pothole.potholelist:
        print(pothole)
    Pothole.update_list()
    print("Potholes:")
    for pothole in Pothole.potholelist:
        print(pothole)

    Pothole("Rue Émile-Ducharme", 275487.25465427524, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    #print(getHierarchyFromName("boulevard de la cité-des-jeunes"))



class Hierarchy(Enum):
    A_DETERMINER = 0
    AUTRE = 1
    ROUTE_LOC = 2
    COLL_SEC = 3
    COLL_PRIM = 4
    ART_SEC = 5
    ART_PRIM = 6
    AUTOROUTE = 7

class Pothole:
    
    potholelist = []
    
    def __init__(self, street_name: str, size: float, long: float, lat: float, birthdate: datetime = 0):
        self.hierarchy = getHierarchyFromName(street_name)
        if (birthdate == 0):
            self.birthdate = datetime.now()
        else:
            self.birthdate = birthdate
        self.street_name = street_name
        self.size = size
        self.long = long
        self.lat = lat
        self.score = 0

    def __repr__(self):
        return f'Pothole({self.hierarchy:20s},{self.birthdate.strftime("%c"):20s},{self.street_name:30s},{self.size/10000:10.5f}dm²,{self.long:3.5f},{self.lat:3.5f},{self.score:3.5f})'
    
    def remove_pothole_from_list(self):
        """_summary_

        Args:
            pothole_id (int): index of pothole
        """
        del Pothole.potholelist[Pothole.potholelist.index(self)]
        
    def add_pothole_to_list(self):
        days_discovered = (datetime.now() - self.birthdate).total_seconds()/(3600*24)
        self.score = getScore(self.hierarchy, days_discovered, self.size)
        Pothole.potholelist.append(self)

    def update_list():
        for pothole in Pothole.potholelist:
            days_discovered = (datetime.now() - pothole.birthdate).total_seconds()/(3600*24)
            pothole.score = getScore(pothole.hierarchy, days_discovered, pothole.size)
        Pothole.potholelist.sort(reverse=True, key=score)


    def biggest_potholes(cls):
        return Pothole.potholelist[:60]

    # def find_score(self):
    #     list_biggest_potholes = []
    #     for pothole in Pothole.potholelist:
    #         list_biggest_potholes.append(pothole)
    #         if len(list_biggest_potholes) >= 60:
    #             return list_biggest_potholes


def score(e):
    return e.score
            

            
__H_SCALE__ = 2.1 # exponent of the hierarchy factor
__T_SCALE__ = 1.2 # exponent of the days passed factor
__T_CONST__ = 1 # constant added to the days since
__S_SCALE__ = 0.4 # exponent of the size factor

def getScore(hierarchy: Hierarchy, days_discovered: float, size: float) -> float:
    return hierarchy.value**__H_SCALE__ * (days_discovered*(math.log10(size)/5)+__T_CONST__)**__T_SCALE__ * (size/1000)**(__S_SCALE__+(math.log10(size)/10))

def getHierarchyFromName(name: str):
    with open("VOIE_PUBLIQUE.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader: 
            if name.lower() == row[8].lower():
                match row[17]:
                    case "Rue locale":
                        return Hierarchy.ROUTE_LOC
                    case "Collectrice secondaire":
                        return Hierarchy.COLL_SEC
                    case "Collectrice principale":
                        return Hierarchy.COLL_PRIM
                    case "Artère secondaire":
                        return Hierarchy.ART_SEC
                    case "Artère principale":
                        return Hierarchy.ART_PRIM
                    case "Autoroute":
                        return Hierarchy.AUTOROUTE
                    case "Autre":
                        return Hierarchy.AUTRE
                    case "À compléter":
                        return Hierarchy.A_DETERMINER
    return "Not Found"


def size_value(size_pothole:float):
    small_size=22500 #15cm **2
    medium_size=90000 #30 cm **2
    max_size =25000000 
    if size_pothole <= small_size:
        return 1
    if medium_size >= size_pothole: # > small_size:
        return 3
    if size_pothole: # > medium_size:
        return 5


app = FastAPI()

@app.post("/upload-file/")
async def result(file: UploadFile = File(...)):
    try:
        extension = file.filename.split(".")[-1]
        if extension not in ["png", "jpg", "bmp", "jpeg"]:
             extension = "jpg"

        # Define a temporary file path
        temp_file_path = f"/tmp-img.{extension}"
        
        # Save the file temporarily
        async with aiofiles.open(temp_file_path, 'wb') as out_file:
            content = await file.read() # async read
            await out_file.write(content) # async write
        
        # Process the file
        nid_de_poule = process_image(temp_file_path)
        
        # Delete the temporary file
        os.remove(temp_file_path)

        if nid_de_poule == None:
             return JSONResponse(
                  status_code=status.HTTP_200_OK,
                  content={"result": 'none'}
             )
        
        Pothole(nid_de_poule["rue"], nid_de_poule["width"]*nid_de_poule["height"], nid_de_poule["lon"], nid_de_poule["lat"]).add_pothole_to_list()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                 "result": 'success',
                 "pothole": nid_de_poule
                 }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
    
@app.get("/get-holes/")
async def get_holes():
    return Pothole.potholelist

@app.get("/update-holes/")
async def update_holes():
    Pothole.update_list()
    return Pothole.potholelist

@app.on_event('shutdown')
async def shutdown():
    with open('pothole.pickle', 'wb') as file: 
        pickle.dump(Pothole.potholelist, file)
    
    pass

@app.on_event("startup")
async def startup():
    try:
        with open('pothole.pickle', 'rb') as file: 
            if(file):
                Pothole.potholelist = pickle.load(file)
        Pothole.update_list()
    except:
        pass
    #main()
    pass

def find_size(cam_distance, pixels, focal_length):
	return pixels * cam_distance / focal_length

def generate_random_string(length):
    # Get all the ASCII letters in lowercase and uppercase
    letters = string.ascii_letters
    # Randomly choose characters from letters for the given length of the string
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def process_image(image_path):

    model = YOLO("model.pt")
    results = model(image_path)
    results[0].save(f"detected/{generate_random_string(10)}.png")
    try:
        x, y, w, h = results[0].boxes.xywh.numpy()[0]
    except IndexError:
         print("Aucun nid de poule trouvé.")
         return None

    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(image_path)

        print(metadata[0])
        
        focal_length = metadata[0]['EXIF:FocalLength']
        subject_distance = metadata[0]['EXIF:SubjectDistance']
        lat_ref = metadata[0]['EXIF:GPSLatitudeRef']
        latitude = metadata[0]['EXIF:GPSLatitude']
        lon_ref = metadata[0]['EXIF:GPSLongitudeRef']
        longitude = metadata[0]['EXIF:GPSLongitude']

        # print(metadata[0])

        real_lat = (-1 if lat_ref == 'S' else 1) * latitude
        real_lon = (-1 if lon_ref == 'W' else 1) * longitude
        width = find_size(subject_distance, w, focal_length)
        height = find_size(subject_distance, h, focal_length)

    url = f"https://nominatim.openstreetmap.org/reverse?lat={real_lat}&lon={real_lon}&format=json"

    rue = requests.get(url).json()["address"]["road"]

    return {
         "rue": rue,
         "lat": real_lat,
         "lon": real_lon,
         "width": width,
         "height": height
    }

#process_image("img-22.jpg")

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

#main()