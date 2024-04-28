from main import Pothole
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from folium import IFrame, folium
from main import Pothole
import base64

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

    encoded = base64.b64encode(open("img-22.jpg", 'rb').read())

    # Add markers for each pothole
    for pothole in potholelist:
        # Create a popup with the coordinates

        html = f'<p>{pothole.lat}, {pothole.long}</p><br><img src="data:image/png;base64,{encoded.decode('UTF-8')}">'
        iframe = IFrame(html)
        popup = folium.Popup(iframe, max_width=2650)

        popup_text = f"Latitude: {pothole.lat}, Longitude: {pothole.long}"
        popup = folium.Popup(popup_text, max_width=250)
        folium.Marker([pothole.lat, pothole.long], popup=popup).add_to(m)

    map_html = m._repr_html_()

    return map_html