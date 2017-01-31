from analysis.plane import PlaneFactory
from db.pghandler import Connection


class RealtimeLoader:
    def __init__(self, db):
        self.db = db

    def getPositionsGJSON(self):
        with Connection(conf=self.db) as c:
            sql = "SELECT * FROM rtstates"
            states = c.selectAll(sql)
        pf = PlaneFactory()
        return {"type": "FeatureCollection",
                "features": [pf.buildPlaneFromSQL(s).getGJSONPlane() for s in states]}
