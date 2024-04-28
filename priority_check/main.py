import csv
#import datetime
from datetime import date, datetime, timedelta
from enum import Enum
import numpy
import math
import exiftool
from ultralytics import YOLO
import requests
from fastapi import FastAPI, UploadFile, File, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import folium
from folium import IFrame
import base64
from PIL import Image
from folium.plugins import HeatMap
import aiofiles
import os
import random
import string
import pickle
from io import BytesIO
from PIL import Image
import base64
import folium
from folium import IFrame
from folium.plugins import HeatMap
import copy

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


class Worker():
    costperkm = 10 # cost per kilometer traveled
    rewardperpothole = 5 # base reward per pothole
    addedrewardperscore = 0.01 # added reward per pothole score
    potholeproxbonusperkm = 0.01 # bonus per 100/(km+1) distance with other potholes
    def __init__(self, long: float, lat: float):
        self.long = long
        self.lat = lat
        self.path = []

def distance_calculator(longitude1, latitude1, longitude2, latitude2):
    """
    R=radius of the earth
    angle1 is the angle of the latitude of the first point in radiant
    angle2 is the angle of the latitude of the second point in radiant
    delta angle: is the angle of the difference between latitudes or longitude 
    returns in km
    """
    R=6371e3
    angle1=latitude1*(numpy.pi/180)
    angle2=latitude2*(numpy.pi/180)
    delta_angle_long=(longitude1-longitude2)*(numpy.pi/180)
    delta_angle_lat=(latitude1-latitude2)*(numpy.pi/180)
    constant_a = numpy.sin(delta_angle_lat/2)*numpy.sin(delta_angle_lat/2) + numpy.cos(angle1)*numpy.cos(angle2)*numpy.sin(delta_angle_long)*numpy.sin(delta_angle_long)
    constant_c = 2 * numpy.arctan2((numpy.sqrt(constant_a)),(numpy.sqrt(1-constant_a)))
    constant_d = R*constant_c
    return constant_d/1000

def pathfind(workers: list):
    workercount = len(workers)
    phlist = copy.deepcopy(Pothole.potholelist)
    iterationcount = 0
    while iterationcount < 20:
        for worker in workers:
            if len(phlist) == 0:
                return
            besthole = Pothole("?", 0, 0, 0)
            bestscore = -100000
            for pothole in phlist:
                score = pf_calc_reward(pothole, phlist, worker) - pf_calc_cost(pothole, worker)
                if score > bestscore:
                    besthole = pothole
                    bestscore = score
            print(besthole)
            worker.path.append(besthole)
            worker.long = besthole.long
            worker.lat = besthole.lat
            phlist.remove(besthole)
        iterationcount += 1



def pf_calc_reward(tpothole: Pothole, potholelist: list, worker: Worker):
    reward = Worker.rewardperpothole + tpothole.score * Worker.addedrewardperscore
    for pothole in potholelist:
        if pothole is tpothole:
            continue
        reward += (100 / (distance_calculator(worker.long, worker.lat, pothole.long, pothole.lat) + 1)) * Worker.potholeproxbonusperkm
    return reward

def pf_calc_cost(tpothole: Pothole, worker: Worker):
    cost = distance_calculator(worker.long, worker.lat, tpothole.long, tpothole.lat) * Worker.costperkm
    return cost


def create_url(coordinates):
    maps_url = 'https://www.google.com/maps/dir/'
    for location in coordinates:
        maps_url += str(location[1]) + ',' + str(location[0]) + '/'
    return maps_url.replace(' ', '%20')
    print(maps_url.replace(' ', '%20'))

def create_link():
    list_link=[]
    list_potholes=Pothole.biggest_potholes()
    list_link.append(list_potholes.pop(0))
    target_lat=list_link[0].lat
    target_long=list_link[0].long
    default_lat=None
    default_long=None
    first_value=distance_calculator(target_long,target_lat,default_long,default_lat)
    fictionnal_value=0
    while fictionnal_value==0:
        for pothole in list_potholes:
            tester_lat=pothole.lat
            tester_long=pothole.long
            test_value=distance_calculator(target_long,target_lat,tester_long,tester_lat)
            if test_value<first_value:
                fictionnal_value=test_value
            else:
                continue
        break
    else:
        while len(list_link) < 10:
            for pothole in list_potholes:
                tester_lat=pothole.lat
                tester_long=pothole.long
                test_value=distance_calculator(target_long,target_lat,tester_long,tester_lat)
                if test_value<fictionnal_value:
                    fictionnal_value=test_value
                else:
                    continue
            else:
                list_link.append(list_potholes.pop(pothole))
        else:
            return list_link
        
def three_point_checker(list_link):
    #find potholes in a grid between point a and point b
    #for potholes in potholes found check distances between two big potholes
    #make a list of those that have only the smallest distance
    #maybe had pathfinding with point base here to be discussed.
    
    active_index=0
    for _ in range(9):
        pothole1=list_link[active_index]
        active_index +=1
        pothole2=list_link[active_index]
        possible_potholes=[]
        lat1=pothole1.lat
        long1=pothole2.long
        lat2=pothole2.lat
        long2=pothole2.long
        for test_pothole in Pothole.potholelist:
            if min(lat1,lat2)<test_pothole.lat<max(lat1,lat2) and min(long1,long2)<test_pothole.long<max(long1,long2):
                possible_potholes.append(test_pothole)
        list_true_subpotholes=[]
        if len(possible_potholes)>4:
            distance_filler=0
            true_subpotholes=[]
            while len(true_subpotholes) !=4:    
                for pothole_variable in possible_potholes:
                    sublat=pothole_variable.lat
                    sublong=pothole_variable.long
                    distance1=distance_calculator(long1,lat1,sublong,sublat)
                    distance2=distance_calculator(sublong,sublat,long2,lat2)
                    distance_total=distance1+distance2
                    if distance_total< distance_filler or distance_filler==0:
                        distance_filler=distance_total
                    else:
                        continue
                else:
                    true_subpotholes.append(distance_filler)
            else:
                list_true_subpotholes.append(true_subpotholes)
        else:
            list_true_subpotholes.append(possible_potholes)
    else:
        return list_true_subpotholes
    

def mixing_line(list_link,list_subpotholes):
    
    final_list=[]
    for x in range(10):
        final_list.append(list_link[x])
        for m in len(list_subpotholes):
            final_list.append(list_subpotholes[x][m])
        else:
            continue
    else:
        return final_list




app = FastAPI()

@app.get("/map", response_class=HTMLResponse)
async def get_map():
    Pothole("Rue de la Coopération", 133729.1393928651, -75.7396333333333, 45.4220305555556).add_pothole_to_list()
    Pothole("Rue de la Coopération", 19014.35597710116, -75.7396333333333, 45.4220305555556).add_pothole_to_list()
    Pothole("Rue de la Coopération", 384329.6356625774, -75.7396333333333, 45.4220305555556).add_pothole_to_list()
    Pothole("Rue de la Coopération", 7544.485864571072, -75.7396333333333, 45.4220305555556).add_pothole_to_list()
    Pothole("Rue de la Coopération", 27337.65215505029, -75.7398916666667, 45.421775).add_pothole_to_list()
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
    Pothole("Rue du Roussillon", 29136.329548451795, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 18841.292545498713, -75.7400027777778, 45.4226527777778).add_pothole_to_list()
    Pothole("Rue de la Coopération", 7621.30828996196, -75.7384194444444, 45.4213666666667).add_pothole_to_list()
    Pothole("Rue de la Coopération", 29282.127129492255, -75.7384694444444, 45.4213861111111).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 13623.072365609714, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 23390.422973778757, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 13502.876965794452, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 15643.786267025705, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 18133.508170100573, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 39539.770553990886, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 44026.590217581426, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 30159.56631893379, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Boulevard Alexandre-Taché", 16071.74704564928, -75.7397055555556, 45.4214527777778).add_pothole_to_list()
    Pothole("Rue Prévost", 27552.365699378373, -75.7427361111111, 45.4201555555556).add_pothole_to_list()
    Pothole("Rue Prévost", 81520.7220137589, -75.7427361111111, 45.4201555555556).add_pothole_to_list()
    Pothole("Rue Prévost", 31795.482396877516, -75.7427361111111, 45.4201555555556).add_pothole_to_list()

    potholelist = Pothole.potholelist

    latitudes=[]
    longitudes=[]
    for pothole in potholelist:
        latitudes.append(pothole.lat)
        longitudes.append(pothole.long)

    # Create a map centered around the first pothole
    m = folium.Map(location=[potholelist[0].lat, potholelist[0].long], zoom_start=13)

    # encoded = base64.b64encode(open("img-22.jpg", 'rb').read())

    # Open the image file
    image = Image.open("img-22.jpg")

    # Define the thumbnail size
    MAX_SIZE = (100, 100)

    # Create the thumbnail
    image.thumbnail(MAX_SIZE)

    # Create a BytesIO object
    im_file = BytesIO()

    # Save the thumbnail to the BytesIO object
    image.save(im_file, format="JPEG")

    # Get the bytes from the BytesIO object
    im_bytes = im_file.getvalue()

    # Encode the bytes to base64
    im_b64 = base64.b64encode(im_bytes)

    # Convert the bytes to a string
    im_b64_str = im_b64.decode('utf-8')

    # Prepare the base64 string for HTML
    base64_html = f"data:image/jpeg;base64,{im_b64_str}"

    points = []

    # Add markers for each pothole
    for pothole in potholelist:
        # Create a popup with the coordinates

        html = f'<p>{pothole.lat}, {pothole.long}</p><br><img src="{base64_html}" style="height: 100%">'
        iframe = IFrame(html, width=300, height=200)
        popup = folium.Popup(iframe, max_width=2650)

        # popup_text = f"Latitude: {pothole.lat}, Longitude: {pothole.long}"
        # popup = folium.Popup(popup_text, max_width=250)
        folium.Marker([pothole.lat, pothole.long], popup=popup).add_to(m)

        points.append([pothole.lat, pothole.long])
    
    HeatMap(points).add_to(m)

    map_html = m._repr_html_()

    return map_html

@app.post("/upload-file/")
async def result(file: UploadFile = File(...)):
    try:
        extension = file.filename.split(".")[-1]
        if extension not in ["png", "jpg", "bmp", "jpeg"]:
             extension = "jpg"


        # Define a temporary file path
        temp_file_path = f"/tmp/tmp-img.{extension}"
        
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
    
@app.get("/pathfind/{count}")
async def pathfind_count(count):
    workers = []
    startcoords = [-75.73872064226423, 45.42243891830577]
    for i in range(0,int(count)):
        workers.append(Worker(startcoords[0], startcoords[1]))
    pathfind(workers)
    result = ""
    for worker in workers:
        pathcoords = [startcoords]
        for pothole in worker.path:
            pathcoords.append([pothole.long, pothole.lat])
        result += create_url(pathcoords) + "\n"
    #print(result)
    #return result
    returned = {}

    for i, res in enumerate(result.split("\n")):
        returned[i] = res
    return returned
    return f"{[(str(worker.path) + ', ') for worker in workers]}"


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
            Pothole.potholelist = pickle.load(file)
        Pothole.update_list()
    except:
        pass
    for pothole in Pothole.potholelist:
        #print(pothole)
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

    print("hello")
    model = YOLO("model.pt")
    print("hello")
    results = model(image_path)
    try:
        _, _, w, h = results[0].boxes.xywh.numpy()[0]
    except IndexError:
         print("Aucun nid de poule trouvé.")
         return None

    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(image_path)
        
        focal_length = metadata[0]['EXIF:FocalLength']
        subject_distance = metadata[0]['EXIF:SubjectDistance']
        lat_ref = metadata[0]['EXIF:GPSLatitudeRef']
        latitude = metadata[0]['EXIF:GPSLatitude']
        lon_ref = metadata[0]['EXIF:GPSLongitudeRef']
        longitude = metadata[0]['EXIF:GPSLongitude']


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

app.mount("/", StaticFiles(directory="../Web-App"), name="web-app")


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

#main()
