# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ResturantItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def __init__(self):
        super().__init__()
        self.fields['url'] = scrapy.Field()
        self.fields['Resturant ID'] = scrapy.Field()
        self.fields['Establishment Name'] = scrapy.Field()
        self.fields['Street Address 1'] = scrapy.Field()
        self.fields['Street Address 2 (shown)'] = scrapy.Field()
        self.fields['City'] = scrapy.Field()
        self.fields['State'] = scrapy.Field()
        self.fields['Zip Code'] = scrapy.Field()
        self.fields['Latitude'] = scrapy.Field()
        self.fields['Longitude'] = scrapy.Field()
        self.fields['Website URL'] = scrapy.Field()
        self.fields['Phone'] = scrapy.Field()
        self.fields['Image Food_1'] = scrapy.Field()
        self.fields['Image Food_2'] = scrapy.Field()
        self.fields['Image Food_3'] = scrapy.Field()
        self.fields['Image Food_4'] = scrapy.Field()
        self.fields['Image Food_5'] = scrapy.Field()
        self.fields['Image Drinks_1'] = scrapy.Field()
        self.fields['Image Drinks_2'] = scrapy.Field()
        self.fields['Image Drinks_3'] = scrapy.Field()
        self.fields['Image Drinks_4'] = scrapy.Field()
        self.fields['Image Drinks_5'] = scrapy.Field()
        self.fields['Image Inside_1'] = scrapy.Field()
        self.fields['Image Inside_2'] = scrapy.Field()
        self.fields['Image Inside_3'] = scrapy.Field()
        self.fields['Image Inside_4'] = scrapy.Field()
        self.fields['Image Inside_5'] = scrapy.Field()
        self.fields['Image Outside_1'] = scrapy.Field()
        self.fields['Image Outside_2'] = scrapy.Field()
        self.fields['Image Outside_3'] = scrapy.Field()
        self.fields['Image Outside_4'] = scrapy.Field()
        self.fields['Image Outside_5'] = scrapy.Field()
        self.fields['Hours Of Operation'] = scrapy.Field()
        self.fields['Price Range'] = scrapy.Field()
        self.fields['Establishment Category'] = scrapy.Field()
        self.fields['Cuisine(s)'] = scrapy.Field()
        self.fields['Top Tags'] = scrapy.Field()
        self.fields['Rating'] = scrapy.Field()
        self.fields['Food Rating'] = scrapy.Field()
        self.fields['Service Rating'] = scrapy.Field()
        self.fields['Ambience Rating'] = scrapy.Field()
        self.fields['Value Rating'] = scrapy.Field()
        self.fields['About Business'] = scrapy.Field()
        self.fields['Neighborhood'] = scrapy.Field()
        self.fields['Cross Streets'] = scrapy.Field()
        self.fields['Dress Code'] = scrapy.Field()
        self.fields['Dining Style'] = scrapy.Field()
        self.fields['Parking Details'] = scrapy.Field()
        self.fields['Payment Options'] = scrapy.Field()
        self.fields['Additional'] = scrapy.Field()



class MoreDetailJsonItem(scrapy.Item):
    def __init__(self):
        super().__init__()
        self.fields['url'] = scrapy.Field()
        self.fields['Resturant ID'] = scrapy.Field()
        self.fields['menuShown'] = scrapy.Field()
        self.fields['menus'] = scrapy.Field()
        self.fields['menuUrl'] = scrapy.Field()
        self.fields['hours'] = scrapy.Field()
    

class HoursCsvItem(scrapy.Item):
    def __init__(self):
        super().__init__()
        self.fields['url'] = scrapy.Field()
        self.fields['Resturant ID'] = scrapy.Field()
        self.fields['Establishment Name'] = scrapy.Field()
        self.fields['Type'] = scrapy.Field()
        self.fields['Monday'] = scrapy.Field()
        self.fields['Tuesday'] = scrapy.Field()
        self.fields['Wednesday'] = scrapy.Field()
        self.fields['Thursday'] = scrapy.Field()
        self.fields['Friday'] = scrapy.Field()
        self.fields['Saturday'] = scrapy.Field()
        self.fields['Sunday'] = scrapy.Field()


class MenuCsvItem(scrapy.Item):
    def __init__(self):
        super().__init__()
        self.fields['url'] = scrapy.Field()
        self.fields['Resturant ID'] = scrapy.Field()
        self.fields['Establishment Name'] = scrapy.Field()
        self.fields['Menu Type'] = scrapy.Field()
        self.fields['Section'] = scrapy.Field()
        self.fields['Section Description'] = scrapy.Field()
        self.fields['Item Title'] = scrapy.Field()
        self.fields['Item Description'] = scrapy.Field()
        self.fields['Item Price'] = scrapy.Field()