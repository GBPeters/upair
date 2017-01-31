class Plane:
    """
    Class for handling Plane data
    """

    def __init__(self, icao, tailnum, country, time_pos, time_vel, lat, lon, alt, ground, vel, heading, vert):
        self.icao = icao
        self.tailnum = tailnum
        self.country = country
        self.time_pos = time_pos
        self.time_vel = time_vel
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.ground = ground
        self.vel = vel
        self.heading = heading
        self.vert = vert

    def getWKT(self):
        """
        Return WKT representation of this Plane's position
        :return: A string containing WKT
        """
        return "POINT (%f %f)" % (self.lon, self.lat)

    def get3DWKT(self):
        """
        Return 3D WKT representation of this Plane's position
        :return: A string containing WKT
        """
        return "POINT (%f %f %f)" % (self.lon, self.lat, self.alt)


class PlaneFactory:
    def __init__(self, plane=None):
        self.plane = plane

    def setPlane(self, plane):
        self.plane = plane
        return self

    def buildPlaneFromSQL(self, sqlresponse):
        icao = sqlresponse[2]
        tailnum = sqlresponse[3]
        country = sqlresponse[4]
        time_pos = sqlresponse[5]
        time_vel = sqlresponse[6]
        lon = sqlresponse[7]
        lat = sqlresponse[8]
        alt = sqlresponse[9]
        ground = sqlresponse[10]
        vel = sqlresponse[11]
        heading = sqlresponse[12]
        vert = sqlresponse[13]
        self.plane = Plane(icao, tailnum, country, time_pos, time_vel, lat, lon, alt, ground, vel, heading, vert)
        return self

    def getGJSONPlane(self):
        p = self.plane
        gjson = {"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [p.lon, p.lat]
                 },
                 "properties": {
                     "id": p.icao,
                     "icao24": p.icao,
                     "callsign": p.tailnum,
                     "country": p.country,
                     "time_pos": p.time_pos,
                     "time_vel": p.time_vel,
                     "altitutde": p.alt,
                     "onground": p.ground,
                     "velocity": p.vel,
                     "heading": p.heading,
                     "vspeed": p.vert
                 }
                 }
        return gjson
