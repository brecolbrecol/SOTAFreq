import maidenhead
import pyproj

class QTH:

    def __init__(self, call_sign, latitude, longitude, locator=None):
        self.call_sign = call_sign
        self.latitude = latitude
        self.longitude = longitude
        self.locator = self.gridLocator() if locator is None else locator

    @classmethod 
    def byLocator(cls, call_sign, locator):
        locator = (locator[:8]) if len(locator) > 8 else locator
        latitude, longitude = maidenhead.to_location(locator, center=True)
        return cls(call_sign, latitude, longitude, locator=locator)

    def gridLocator(self):
        return maidenhead.to_maiden(self.latitude, self.longitude, precision=4)

    def __str__(self):
        return f'{self.locator}'

    def calculate_bearings(self, other):
        geodesic = pyproj.Geod(ellps='WGS84')
        fwd_azimuth, back_azimuth, distance = geodesic.inv(self.longitude, self.latitude, other.longitude,
                                                           other.latitude)
        return [fwd_azimuth, back_azimuth, distance]