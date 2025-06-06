#!/usr/bin/env python3
from Summit import Summit
from QTH import QTH
from Summit import Summit
import csv
import re

class SOTAFile:
    
    QTHs = {}
    MY_QTH = None
    INFO = {}
    
    @classmethod
    def loadV2(cls, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                other_locator = None
                call_sign = row[1]
                reference = row[2]
                other_call_sign = row[7]
                other_sota_reference = row[8]
                match_locator = re.search("[A-R]{2}[0-9]{2}[a-w]{2}[0-9]*", row[9], flags=re.IGNORECASE)
                if match_locator:
                    other_locator = match_locator.group()

                if (cls.MY_QTH == None):
                    cls.MY_QTH = Summit(reference, activator=call_sign)
                if (other_sota_reference != ''):
                    cls.QTHs[other_call_sign] = Summit(other_sota_reference, activator=other_call_sign)
                if (other_locator != None):
                    cls.QTHs[other_call_sign] = QTH.byLocator(other_call_sign, other_locator)
                    
    @classmethod
    def calculateDistances(cls):
        distances = {}
        for other_call_sign in sorted(cls.QTHs.keys()):
            qth = cls.QTHs[other_call_sign]
            fwd_azimuth, back_azimuth, distance = qth.calculate_bearings(cls.MY_QTH)
            distances[qth.call_sign] = distance
        return distances
            

SOTAFile.loadV2(filename="/home/jorge.anton/tmp/EA2BD_20230701_SOTA.csv")
# SOTAFile.loadV2(filename="/home/jorge.anton/tmp/EA4HFO_20230701_SOTA.csv")
distances = SOTAFile.calculateDistances()
print("QSOs from " + SOTAFile.MY_QTH.reference + " (" + SOTAFile.MY_QTH.gridLocator() + ") " + SOTAFile.MY_QTH.activator + ":")
distances_sorted = sorted(distances.items(), key=lambda x:x[1], reverse=True)
converted_dict = dict(distances_sorted)

count=1
for other_call_sign in converted_dict.keys():
    distance = converted_dict[other_call_sign]
    print("{:<1}.\t{:<10}\t".format(count, other_call_sign) + "{:.2f} km\t".format(round((distance / 1000), 2)) + str(SOTAFile.QTHs[other_call_sign]))
    count += 1