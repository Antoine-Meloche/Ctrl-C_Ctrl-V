import csv
#import datetime
from datetime import date, datetime
from enum import Enum

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


    Pothole("Rue du Roussillon", 65178.743932303616, -75.7406833333333, 45.4243027777778).add_pothole_to_list()
    print(Pothole.potholelist)
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
    
    def __init__(self, street_name: str, size: float, long: float, lat: float):
        self.hierarchy = getHierarchyFromName(street_name)
        self.birthdate = datetime.now
        self.street_name = street_name
        self.size = size
        self.long = long
        self.lat = lat
        self.score = 0
    
    def remove_pothole_from_list(self):
        """_summary_

        Args:
            pothole_id (int): index of pothole
        """
        del Pothole.potholelist[Pothole.potholelist.index(self)]
        
    def add_pothole_to_list(self):
        hierarchy = self.hierarchy
        days_discovered = (datetime.now() - self.birthdate).total_seconds()/(3600*24)
        self.score = getScore(hierarchy,days_discovered)
        Pothole.potholelist.append(self)

    def update_list(cls):
        for pothole in Pothole.potholelist:
            pothole.score = getScore(pothole.hierarchy, pothole.days_discovered)
        Pothole.potholelist.sort(reverse=True, key=score)


    def find_score(cls):
        list_biggest_potholes = []
        for pothole in Pothole.potholelist:
            list_biggest_potholes.append(pothole)
            if len(list_biggest_potholes) >= 60:
                return list_biggest_potholes


def score(e):
    return e.score
            
            
                
            
__H_SCALE__ = 2
__T_SCALE__ = 1.2
__T_CONST__ = 1

def getScore(hierarchy: Hierarchy, days_discovered: float) -> float:
    return int(hierarchy)**__H_SCALE__ * (days_discovered+__T_CONST__)**__T_SCALE__

def getHierarchyFromName(name: str):
    with open("VOIE_PUBLIQUE.csv", newline='', encoding="utf-8") as csvfile:
        typelist = []
        potholelist = []
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
    small_size=None
    medium_size=None
    if size_pothole <= small_size:
        return 1
    if medium_size >= size_pothole: # > small_size:
        return 3
    if size_pothole: # > medium_size:
        return 5


if __name__ == "__main__":
    main()
