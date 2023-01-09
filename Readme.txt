Opentable Scrapper

Requirements
------------------------------------------------------------
PYTHON >= 3.6
scrapy


Steps to Run the crawler
-----------------------------------------------
Run command "scrapy crawl resturants -O filename.csv"

To Change output filenames, edit "RESTURANT_FILENAME" field in settings.py file
To Change menu and hours filenames, edit "MENU_FILENAME" field in settings.py file

Note
--------------------------------------------------------------
Keep "OpenTable-CityList.csv" in same folder structure (same as scrapy.cfg)