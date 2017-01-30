import os

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="UpAir",
    version="0.1",
    author="Team Maja - Simon Veen & Gijs Peters",
    author_email="simon.veen@wur.nl",
    description=("Team Maja's Geo-Scripting project about airplanes!"),
    license="GPL-3.0",
    keywords="geo scripting airplanes",
    url="http://github.com/GBPeters/upair",
    packages=['bot', 'db', 'map'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPL-3.0"
    ],
    install_requires=['flask', 'psycopg2', 'werkzeug', 'BeautifulSoup4']
)
