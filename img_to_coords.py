import exiftool
from ultralytics import YOLO
import requests

model = YOLO("model.pt")
# for i in range(1, 7):
#     results = model(f"img-{i}.jpg")

#     print(results)

def find_size(cam_distance, pixels, focal_length):
	return pixels * cam_distance / focal_length

file = "img-1.jpg"
with exiftool.ExifToolHelper() as et:
    metadata = et.get_metadata(file)
    
    focal_length = metadata[0]['EXIF:FocalLength']
    subject_distance = metadata[0]['EXIF:SubjectDistance']
    lat_ref = metadata[0]['EXIF:GPSLatitudeRef']
    latitude = metadata[0]['EXIF:GPSLatitude']
    lon_ref = metadata[0]['EXIF:GPSLongitudeRef']
    longitude = metadata[0]['EXIF:GPSLongitude']

    # print(metadata[0])

    print((-1 if lat_ref == 'S' else 1) * latitude)
    print((-1 if lon_ref == 'W' else 1) * longitude)
    print(find_size(subject_distance, 100, focal_length))

url = f"https://nominatim.openstreetmap.org/reverse?lat={(-1 if lat_ref == 'S' else 1) * latitude}&lon={(-1 if lon_ref == 'W' else 1) * longitude}&format=json"

print(requests.get(url).json()["address"]["road"])