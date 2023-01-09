# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from .items import ResturantItem, MoreDetailJsonItem, MenuCsvItem, HoursCsvItem
import scrapy
import json

class OpentablePipeline:
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline:

    def __init__(self):
        self.resturant_ids_seen = set()
        self.more_details_ids_seen = set()
        self.menu_ids_seen = set()
        self.hours_ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if isinstance(item, ResturantItem):
            if adapter['url'] in self.resturant_ids_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.resturant_ids_seen.add(adapter['url'])
                return item

        elif isinstance(item, MoreDetailJsonItem):
            if adapter['url'] in self.more_details_ids_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.more_details_ids_seen.add(adapter['url'])
                return item
        
        elif isinstance(item, MenuCsvItem):
            if f"{adapter['url']}{adapter['Menu Type']}{adapter['Section']}{adapter['Item Title']}" in self.menu_ids_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.menu_ids_seen.add(f"{adapter['url']}{adapter['Menu Type']}{adapter['Section']}{adapter['Item Title']}")
                return item
        
        elif isinstance(item, HoursCsvItem):
            if f"{adapter['url']}{adapter['Type']}" in self.hours_ids_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.hours_ids_seen.add(f"{adapter['url']}{adapter['Type']}")
                return item


class DownloadImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, ResturantItem):
            rid = item['Resturant ID']
            for k, v in item.items():
                if 'Image' in k and v:
                    url = v
                    ext = url.split('.')[-1]
                    type = k.replace("Image","").strip().lower()
                    path = f"{rid}/{rid}_{type}.{ext}"
                    yield scrapy.Request(url, meta={'image_path':path}, dont_filter=True)

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{request.meta["image_path"]}'


import csv
import os
from .settings import RESTURANT_FILENAME, MENU_CSV_FILENAME, HOURS_CSV_FILENAME, MENU_FILENAME, RESTURANT_FIELDS, MENU_FIELDS, HOURS_FIELDS

class SaveMoreDetailPipeline:

    def open_spider(self, spider):
        self.file = open(MENU_FILENAME, 'w')
        # Your scraped items will be saved in the file 'scraped_items.json'.
        # You can change the filename to whatever you want.
        self.file.write("{")

        self.resturant_csvwriter = csv.writer(open(RESTURANT_FILENAME, 'w', encoding='utf-8-sig'), lineterminator='\n')
        self.resturant_csvwriter.writerow(RESTURANT_FIELDS)

        self.menu_csvwriter = csv.writer(open(MENU_CSV_FILENAME, 'w', encoding='utf-8-sig'), lineterminator='\n')
        self.menu_csvwriter.writerow(MENU_FIELDS)

        self.hours_csvwriter = csv.writer(open(HOURS_CSV_FILENAME, 'w', encoding='utf-8-sig'), lineterminator='\n')
        self.hours_csvwriter.writerow(HOURS_FIELDS)


    def close_spider(self, spider):
        # self.file.seek(-2, os.SEEK_END)
        # self.file.truncate()
        self.file.close()
        
        with open(MENU_FILENAME, 'rb+') as filehandle:
            filehandle.seek(-3, os.SEEK_END)
            filehandle.truncate()
        
        with open(MENU_FILENAME, 'a') as filehandle:
            filehandle.write("\n}")

        # file = open(MENU_FILENAME, 'w')
        # file.write("}")
        # file.close()



    def process_item(self, item, spider):
        if isinstance(item, MoreDetailJsonItem):
            line = '\n"' + str(item['Resturant ID']) + '"' + ":" + json.dumps(
                dict(item),
                indent = 4,
                separators = (',', ': ')
            ) + ",\n"
            self.file.write(line)
        
        elif isinstance(item, ResturantItem):
            self.resturant_csvwriter.writerow([item.get(key, '') for key in RESTURANT_FIELDS])
        
        elif isinstance(item, MenuCsvItem):
            self.menu_csvwriter.writerow([item.get(key, '') for key in MENU_FIELDS])
        
        elif isinstance(item, HoursCsvItem):
            self.hours_csvwriter.writerow([item.get(key, '') for key in HOURS_FIELDS])
        
        return item

