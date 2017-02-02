# Up in the Air

#### Final Project for the WUR-course on Geo-Scripting (GRS-33806)
##### Team Maja - Simon Veen & Gijs Peters

This project harvests realtime flight data, creates flightpaths,
and sets up a webserver for displaying this information realtime on a Leaflet surface.
 
It contains two apps, `bot/app.py` and `map/app.py`.
The first starts up a harvesting bot for harvesting and processing
aircraft data.

The second starts a Flask webserver hosting a Leaflet map for displaying
these data near-realtime.

#### Install instructions
to install on a clean Ubuntu 16.04 machine, open your terminal, and execut the lines below:
```bash
mkdir git
cd git
git clone http://github.com/GBPeters/upair
cd upair
chmod +x install_upair.sh
./install_upair.sh
```

A PostgreSQL/PostGIS will be set up for local use, and required tables and roles will be created.
Now, to start up the harvesting bot, use:
```bash
python bot/app.py opensky -i 50
```
This will start an OpenSky network harvester with harvest interval of 50 seconds

*NOTE: setting this interval to less than 10 seconds will result in an IP-block.*

If you have collected some data, fire up the webserver with
```bash
python map/app.py
```
Open your browser and surf to <http://localhost:5000>

If something goes wrong during installation, or you need help, feel free to contact us.