#!/usr/bin/env python3
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
        kml.altitudemode = simplekml.AltitudeMode.absolute
        kml.networklinkcontrol.minrefreshperiod = 1 
        for summit in Summit.summits.values():
            description = summit.name + " (" + str(summit.altitude) + "m) - " + summit.activator + ", " + summit.freq
            point = kml.newpoint(description=description,name=summit.reference,
                         coords=[(summit.longitude, summit.latitude,summit.altitude)])  # lon, lat, optional height
            point.style.iconstyle.icon.href = 'https://sota.jorge.red/pointers/icon' + str(summit.points) + '.png'
        # save KML to a file
        kml.save("test.kml")
        
    @staticmethod
    def parse_csv():
        with open('inscripcion_2023.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                reference = row['Número de la cima (si ya la has elegido)']
                activator = row['TU INDICATIVO con el que participarás (en mayúsculas)']
                if reference in Summit.summits:
                    Summit.summits[reference].activator += ", " + activator
                    print("INFO: new " + reference + " activators: " + Summit.summits[reference].activator)
                else:
                    Summit(reference, activator=activator)
            
    @staticmethod
    def generate_csv_frequencies():
        with open('frecuencias_asignadas.csv', 'w') as f_assigned_freqs:
            fieldnames = ['SOTA_reference', 'frequency', 'call_sign(s)']
            writer = csv.DictWriter(f_assigned_freqs, fieldnames=fieldnames, delimiter=";")

            writer.writeheader()
            for summit in Summit.summits.values():
                writer.writerow({'SOTA_reference': summit.reference, 'frequency': summit.freq, 'call_sign(s)': summit.activator})

    def load_attributes_from_api(self):
        api_data = urllib.request.urlopen("https://api2.sota.org.uk/api/summits/" + self.reference ).read()
        return json.loads(api_data.decode('utf-8'))
    
    def __init__(self, reference, activator=None, freq=None):
        if reference in Summit.summits:
            raise Exception("ERROR: " + reference  + " already exists")
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
        else:
            print("WARNING: no free frequency for " + self.reference) # ToDo: implement freq reuse algorithm 

        Summit.summits[self.reference] = self
        
if __name__ == "__main__":
    print("Free frequencies before assigment: (" + str(len(Summit.available_frequencies)) + ") " + str(Summit.available_frequencies))
    summits = Summit.parse_csv()
    print("Free frequencies after assigment: (" + str(len(Summit.available_frequencies)) + ") " + str(Summit.available_frequencies))
    
    print("\nGenerating KML... ", end='')
    Summit.create_kml_of_summits()
    print("DONE")
    
    print("Generating CSV... ", end='')
    Summit.generate_csv_frequencies()
    print("DONE")

    print("\nTOTAL SUMMITS: " + str(len(Summit.summits.values())))
    for summit in Summit.summits.values():
        print(summit.reference + ": " + summit.freq, end=', ')
    print("")
