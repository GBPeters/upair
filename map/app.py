import webbrowser
from threading import Thread

from map.mapserver import app


class MapThread(Thread):
    def run(self):
        app.run()


if __name__ == '__main__':
    MapThread().start()
    webbrowser.open("http://localhost:5000", new=2)
