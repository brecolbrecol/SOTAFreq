import urllib.request
import json
import simplekml
import csv
from pprint import pprint

class Summit:
    summits = {}
    available_frequencies = ["145.400","145.425","145.450","145.475","145.525","145.550","145.575","145.200","145.225","145.250","145.275","145.300","145.325","145.350","145.375","144.525", "144.550", "144.575", "144.625", "144.725", "144.750", "144.775"]
    
    @staticmethod
    def create_kml_of_summits():
        kml = simplekml.Kml()
        for summit in Summit.summits.values():
            description = summit.name + " (" + str(summit.altitude) + "m) - " + summit.activator + ", " + summit.freq
            kml.newpoint(description=description,name=summit.reference,
                         coords=[(summit.longitude, summit.latitude,summit.altitude)])  # lon, lat, optional height
            kml.altitudemode = simplekml.AltitudeMode.absolute
        # save KML to a file
        kml.save("test.kml")
        
    @staticmethod
    def parse_csv():
        with open('inscripcion_2023.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                reference = row['Número de la cima (si ya la has elegido)']
                activator = row['TU INDICATIVO con el que participarás (en mayúsculas)']
                Summit(reference, activator=activator)
            print("Free frequencies: " + str(Summit.available_frequencies))

    def load_attributes_from_api(self):
        api_data = urllib.request.urlopen("https://api2.sota.org.uk/api/summits/" + self.reference ).read()
        return json.loads(api_data)
        
    def __init__(self, reference, activator=None, freq=None):
        self.reference = reference # Summit reference
        self.activator = activator
        self.api_data_raw = self.load_attributes_from_api() # All data retreived from API
        
        self.altitude = self.api_data_raw["altM"] # Altitude, in meters above sea level
        self.latitude = self.api_data_raw["latitude"]
        self.longitude = self.api_data_raw["longitude"]
        self.name = self.api_data_raw["name"]
        self.region = self.api_data_raw["regionName"]
        self.reference = self.api_data_raw["summitCode"]
        self.points = self.api_data_raw["points"]
        self.valid = self.api_data_raw["valid"]

        if Summit.available_frequencies:
            self.freq = Summit.available_frequencies.pop()
            print(self.reference + ";" + self.freq)
        else:
            print("WARNING: no free frequencies for " + self.reference)

        Summit.summits[self.reference] = self
        
if __name__ == "__main__":
    summits = Summit.parse_csv()
    Summit.create_kml_of_summits()