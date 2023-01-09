Opentable Scrapper

Requirements
------------------------------------------------------------
PYTHON >= 3.6
scrapy


Steps to Run the crawler
-----------------------------------------------
Run command "scrapy crawl resturants"

To Change output filenames, edit "RESTURANT_FILENAME" field in settings.py file
To Change menu and hours filenames, edit "MENU_FILENAME" field in settings.py file
To Change menu csv filename, edit "MENU_CSV_FILENAME" field in settings.py file
To Change hours csv filename, edit "HOURS_CSV_FILENAME" field in settings.py file

Note
--------------------------------------------------------------
Keep "OpenTable-CityList.csv" in same folder structure (same as scrapy.cfg)