#!/usr/bin/env python3
import csv
import json
import urllib.request
from pprint import pprint

import simplekml
from QTH import QTH
from FrequenciesAssign import FrequenciesAssign


class Summit(QTH):
    summits = {}
    set_available_frequencies = [
        "145.400", "145.425", "145.450", "145.475", "145.525", "145.550", "145.200", "145.225", "145.250",
        "145.275", "145.300", "145.325", "145.350", "145.375", "144.525", "144.550", "144.575", "144.625", "144.725",
        "144.750", "144.775"
    ]
    available_frequencies = set_available_frequencies.copy()

    @classmethod
    def create_kml_of_summits(cls):
        kml = simplekml.Kml()
        kml.altitudemode = simplekml.AltitudeMode.absolute
        kml.networklinkcontrol.minrefreshperiod = 1
        for summit in cls.summits.values():
            description = summit.activator + ", " + summit.freq + " - " + summit.reference + " (" + str(
                summit.altitude) + "m)"
            point = kml.newpoint(description=description,
                                 name=summit.name,
                                 coords=[(summit.longitude, summit.latitude, summit.altitude)
                                        ])  # lon, lat, optional height
            point.style.iconstyle.icon.href = 'https://sota.jorge.red/pointers/icon' + str(summit.points) + '.png'
            point.style.labelstyle.color = simplekml.Color.white
            point.style.labelstyle.scale = 1.1
            point.extendeddata.newdata(name="freq", value=summit.freq, displayname="Frecuencia")
            point.extendeddata.newdata(name="activator", value=summit.activator, displayname="Activador(es)")
            point.extendeddata.newdata(name="altitude", value=summit.altitude, displayname="Altitud")
            point.extendeddata.newdata(name="points", value=summit.points, displayname="Puntos")
        # save KML to a file
        kml.save("test.kml")

    @classmethod
    def generate_csv_frequencies(cls):
        with open('frecuencias_asignadas.csv', 'w') as f_assigned_freqs:
            fieldnames = ['SOTA_reference', 'frequency', 'call_sign(s)']
            writer = csv.DictWriter(f_assigned_freqs, fieldnames=fieldnames, delimiter=";")

            writer.writeheader()
            for summit_reference in sorted(cls.summits.keys()):
                summit = cls.summits[summit_reference]
                writer.writerow({
                    'SOTA_reference': summit.reference,
                    'frequency': summit.freq,
                    'call_sign(s)': summit.activator
                })

    def load_attributes_from_api(self):
        try:
            api_data = urllib.request.urlopen("https://api2.sota.org.uk/api/summits/" + self.reference).read()
            return json.loads(api_data.decode('utf-8'))
        except Exception as e: print("https://api2.sota.org.uk/api/summits/" + self.reference + " -> " + str(e))

    def __init__(self, reference, activator=None, freq=None):

        if reference in Summit.summits:
            raise Exception("ERROR: " + reference + " already exists")
        self.reference = reference  # Summit reference
        self.activator = activator
        self.api_data_raw = self.load_attributes_from_api()  # All data retreived from API
        super().__init__(activator, self.api_data_raw["latitude"], self.api_data_raw["longitude"])
        self.altitude = self.api_data_raw["altM"]  # Altitude, in meters above sea level
        self.name = self.api_data_raw["name"]
        self.region = self.api_data_raw["regionName"]
        self.reference = self.api_data_raw["summitCode"]
        self.points = self.api_data_raw["points"]
        self.valid = self.api_data_raw["valid"]
        self.freq = freq

    def __str__(self):
        return f'{self.reference}'

    @classmethod
    def fromCSV(cls, filename='inscritos_2024.csv'):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                reference = row.get('CIMA')
                activator = row.get('ACTIVADOR')
                freq = row.get('FRECUENCIA')
                if reference in cls.summits:
                    cls.summits[reference].activator += ", " + activator
                    print("INFO: new " + reference + " activators: " + cls.summits[reference].activator)
                else:
                    try:
                        if reference :
                            new_summit = cls(reference, activator=activator, freq=freq)
                            cls.summits[reference] = new_summit
                    except:
                        print("WARNING: ignoring reference " + str(reference))


if __name__ == "__main__":
    print("Free frequencies before assigment: (" + str(len(FrequenciesAssign.frequencies_2m_fm)) + ") " +
          str(FrequenciesAssign.frequencies_2m_fm))
    Summit.fromCSV()
    Summit.summits = FrequenciesAssign().generate(Summit.summits)
    print("Free frequencies after assigment: (" + str(len(FrequenciesAssign.frequencies_2m_fm)) + ") " +
          str(FrequenciesAssign.frequencies_2m_fm))

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

    print("\nGenerating bearings... ", end='')
    with open('bearing.txt', 'w') as f_bearing:
        f_bearing.write("# BEARINGS\n")
        for summit_reference in sorted(Summit.summits.keys()):
            summit = Summit.summits[summit_reference]
            f_bearing.write("\n## FROM " + summit_reference + " - " + summit.name + " (" + str(summit.altitude) +
                            " msnm) [" + str(summit.points) + " pts]\n")
            f_bearing.write("SUMMIT REF\tFORWARD\tBACK\tFREQUENCY\tDISTANCE & ACTIVATOR(S)\n")
            for other_summit_reference in sorted(Summit.summits.keys()):
                other_summit = Summit.summits[other_summit_reference]
                fwd_azimuth, back_azimuth, distance = summit.calculate_bearings(other_summit)
                f_bearing.write(other_summit_reference + "\t" + str(round(fwd_azimuth, 2)) + "\t" +
                                str(round(back_azimuth, 2)) + "\t" + other_summit.freq + " MHz\t" +
                                str(round((distance / 1000), 2)) + " km  " + other_summit.activator + "\n")
    print("DONE")
