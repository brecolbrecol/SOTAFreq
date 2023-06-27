import urllib.request
import json
from pprint import pprint

class Summit:
    summits = {}
    
    def load_attributes_from_api(self):
        api_data = urllib.request.urlopen("https://api2.sota.org.uk/api/summits/" + self.reference ).read()
        return json.loads(api_data)
        
    def __init__(self, reference, call=None, freq=None):
        self.reference = reference # Summit reference
        self.api_data_raw = self.load_attributes_from_api() # All data retreived from API
        self.altitude = self.api_data_raw["altM"] # Altitude, in meters above sea level
        self.latitude = self.api_data_raw["latitude"]
        self.longitude = self.api_data_raw["longitude"]
        self.name = self.api_data_raw["name"]
        self.region = self.api_data_raw["regionName"]
        self.reference = self.api_data_raw["summitCode"]
        self.points = self.api_data_raw["points"]
        self.valid = self.api_data_raw["valid"]
        
if __name__ == "__main__":
    maliciosa = Summit("ea4/md-007")
    pprint(vars(maliciosa))