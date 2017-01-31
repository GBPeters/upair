from db.pghandler import Connection

class Plane:
    def __init__(self, id, icao, tailnum, country, time_pos, time_vel, lat, lon, alt, ground, vel, heading, vert):
        self.id = id
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


with Connection() as c:
    states = c.selectAll("SELECT * FROM states Limit 10000")
    planes = []
    for s in states:
        print s
        id = s[0]
        icao = s[2]
        tailnum = s[3]
        country = s[4]
        time_pos = s[5]
        time_vel = s[6]
        lon = s[7]
        lat = s[8]
        alt = s[9]
        ground = s[10]
        vel = s[11]
        heading = s[12]
        vert = s[13]
        plane = Plane(id, icao, tailnum, country, time_pos, time_vel, lat, lon, alt, ground, vel, heading, vert)
        planes += [plane]

print planes[1].heading





