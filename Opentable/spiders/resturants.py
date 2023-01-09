import scrapy
import json
import csv
from ..items import ResturantItem, MoreDetailJsonItem, MenuCsvItem, HoursCsvItem
from ..utils import *
from ..settings import MENU_FILENAME


class ResturantsSpider(scrapy.Spider):
    name = 'resturants'
    allowed_domains = ['www.opentable.com']
    start_urls = ['http://www.opentable.com/']

    unfound_locations = []
    auto_sha = get_auto_sha()
    multi_sha = get_multi_sha()
    photo_sha = get_photo_sha()


    def parse(self, response):
        start = response.text.find('__CSRF_TOKEN__')
        a = response.text.find("=",start)
        z = response.text.find(';',start)
        csrf = response.text[a:z].replace('=','').replace('"','').replace("'",'')

        url = 'https://www.opentable.com/dapi/fe/gql?optype=query&opname=Autocomplete'

        headers = {
                    'x-csrf-token': csrf,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                    'origin': 'https://www.opentable.com',
                    'content-type' : 'application/json;charset=utf-8'
                }

        meta = response.meta
        meta['csrf'] = csrf
        with open('OpenTable-CityList.csv', 'r', encoding='utf-8-sig') as file:
            csvFile = csv.reader(file)
            next(csvFile, None)
            for city in csvFile:
                data = get_city_data(city[0].split(',')[0], self.auto_sha)
                meta['city'] = city
                yield scrapy.Request(url, method='POST', body=json.dumps(data), headers=headers, callback=self.parse_city, meta=meta, dont_filter=True)
                break
         

    def parse_city(self, response):
        try:
            data = json.loads(response.text)

            headers = {
                        'x-csrf-token': response.meta['csrf'],
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                        'origin': 'https://www.opentable.com',
                        'content-type' : 'application/json;charset=utf-8'
                    }
            url = 'https://www.opentable.com/dapi/fe/gql?optype=query&opname=MultiSearchRestaurants'

            found_location = False
            for result in data['data']['autocomplete']['autocompleteResults']:
                if result['type'] == 'Location' and result['metroId']:
                    found_location = True
                    data = get_multisearch_data(result['metroId'], self.multi_sha)
                    yield scrapy.Request(url, method='POST', body=json.dumps(data), headers=headers, callback=self.parse_listing, meta=response.meta, dont_filter=True)

            if not found_location:
                self.unfound_locations.append(response.meta['city'])
        except Exception as e:
            print('parse_city', e)


    def parse_listing(self, response):
        try:
            data = json.loads(response.text)
            headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                    }

            for resturant in data['data']['restaurantSearch']['restaurants']:
                url = resturant['urls']['profileLink']['link']
                yield scrapy.Request(url, headers=headers, callback=self.parse_resturant, meta=response.meta)
                

        except Exception as e:
            print('parse_listing',e)


    def parse_resturant(self, response):
        try:
            script = response.xpath('//script[contains(text(), "__INITIAL_STATE__")]/text()').get()

            start = script.find('__INITIAL_STATE__')
            a = script.find('{', start)
            z = script.find('};', start)
            data = json.loads(script[a:z+1])

            resturant = data['restaurantProfile']


            headers = {
                        'x-csrf-token': response.meta['csrf'],
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                        'origin': 'https://www.opentable.com',
                        'content-type' : 'application/json;charset=utf-8'
                    }

            url = 'https://www.opentable.com/dapi/fe/gql?optype=query&opname=photoGallery'
            data = get_image_data(resturant['restaurant']['restaurantId'], self.photo_sha)
            yield scrapy.Request(url, method='POST', body=json.dumps(data), headers=headers, callback=self.parse_images, 
                                                meta=response.meta, dont_filter=True, cb_kwargs={'resturant':resturant, 'url': response.url})
        except Exception as e:
            print('parse_resturant', e)


    def parse_images(self, response, resturant, url):
        menus = resturant['menus']
        resturant = resturant['restaurant']
        try:
            images = json.loads(response.text)['data']['restaurant']['photos']['gallery']['photos']

            item = ResturantItem()
            resturant_id = str(get_value(resturant, ['restaurantId']))
            resturant_name = get_value(resturant, ['name'])

            item['url'] = url
            item['Resturant ID'] = resturant_id
            item['Establishment Name'] = resturant_name
            item['Street Address 1'] = get_value(resturant, ['address', 'line1'])
            item['Street Address 2 (shown)'] = get_value(resturant, ['address','line2'])
            item['City'] = get_value(resturant, ['address','city'])
            item['State'] = get_value(resturant, ['address','state'])
            item['Zip Code'] = get_value(resturant, ['address','postCode'])
            item['Latitude'] = get_value(resturant, ['coordinates','latitude'])
            item['Longitude'] = get_value(resturant, ['coordinates','longitude'])
            item['Website URL'] = get_value(resturant, ['website'])
            item['Phone'] = get_value(resturant, ['contactInformation','formattedPhoneNumber'])

            for _ in range(5):
                item[f'Image Food_{_+1}'] = ''
            for _ in range(5):
                item[f'Image Drinks_{_+1}'] = ''
            for _ in range(5):
                item[f'Image Inside_{_+1}'] = ''
            for _ in range(5):
                item[f'Image Outside_{_+1}'] = ''
            
            image_list = get_images(images)

            for i, photo in enumerate(image_list['food']):
                item[f'Image Food_{i+1}'] = photo
            
            for i, photo in enumerate(image_list['drinks']):
                item[f'Image Drinks_{i+1}'] = photo
            
            for i, photo in enumerate(image_list['interior']):
                item[f'Image Inside_{i+1}'] = photo

            for i, photo in enumerate(image_list['exterior']):
                item[f'Image Outside_{i+1}'] = photo

            item['Hours Of Operation'] = get_value(resturant, ['hoursOfOperation']).replace('<br />','').replace('\n', ' ')
            
            item['Price Range'] = get_value(resturant, ['priceBand', 'name'])
            item['Establishment Category'] = get_value(resturant, ['primaryCuisine', 'name'])

            cusines = []
            for cus in resturant.get('cuisines', {}):
                cusines.append(cus.get('name',''))
            
            cusines = ', '.join(cusines) if cusines else ''
            item['Cuisine(s)'] = cusines.strip()

            tags = []
            for tag in get_value(resturant, ['statistics','reviews','categories']):
                tags.append(tag.get('category',{}).get('name',''))
            tags = ', '.join(tags) if tags else ''
            item['Top Tags'] = tags.strip()

            item['Rating'] = get_value(resturant, ['statistics','reviews','ratings','overall','rating'])
            item['Food Rating'] = get_value(resturant, ['statistics','reviews','ratings','food','rating'])
            item['Service Rating'] = get_value(resturant, ['statistics','reviews','ratings','service','rating'])
            item['Ambience Rating'] = get_value(resturant, ['statistics','reviews','ratings','ambience','rating'])
            item['Value Rating'] = get_value(resturant, ['statistics','reviews','ratings','value','rating'])
            item['About Business'] = get_value(resturant, ['description'])
            item['Neighborhood'] = get_value(resturant, ['neighborhood', 'name'])
            item['Cross Streets'] = get_value(resturant, ['crossStreet'])
            item['Dress Code'] = get_value(resturant, ['dressCode'])
            item['Dining Style'] = get_value(resturant, ['diningStyle'])
            parking = resturant['parkingDetails']
            if not parking:
                parking = resturant['parkingInfo']
            item['Parking Details'] = parking
            item['Payment Options'] = ', '.join(resturant.get('paymentOptions', []))
            item['Additional'] = ', '.join(resturant.get('additionalDetails', []))

            yield item

            more = MoreDetailJsonItem()
            menu_info = menus['menuInfo']
            more['url'] = url
            more['Resturant ID'] = resturant_id

            if menu_info['showThirdPartyMenu']:
                if menus['menuData']:
                    more['menuShown'] = True
                    menu_dict = get_menu(menus['menuData'])
                    more['menus'] = menu_dict
                    
            
                    for menu_type in menu_dict:
                        menuType = menu_type['menuType']
                        for section in menu_type['sections']:
                            section_name = section['sectionType']
                            section_desc = section['description']
                            for section_item in section['items']:
                                menu_csv = MenuCsvItem()
                                menu_csv['url'] = url
                                menu_csv['Resturant ID'] = resturant_id
                                menu_csv['Establishment Name'] = resturant_name
                                menu_csv['Menu Type'] = menuType
                                menu_csv['Section'] = section_name
                                menu_csv['Section Description'] = section_desc
                                menu_csv['Item Title'] = section_item['title']
                                menu_csv['Item Description'] = section_item['description']
                                menu_csv['Item Price'] =  section_item['price']
                                yield menu_csv
                    
                else:
                    more['menuShown'] = False
                    more['menuUrl'] = 'NA' if not menu_info['url'] else menu_info['url'] 
            else:
                more['menuShown'] = False
                more['menuUrl'] = menu_info['url']

    
            hours_dict = parse_hours(get_value(resturant, ['hoursOfOperation']))
            more['hours'] = hours_dict

            for hour in hours_dict:
                hour_csv = HoursCsvItem()
                hour_csv['url'] = url
                hour_csv['Resturant ID'] = resturant_id
                hour_csv['Establishment Name'] = resturant_name
                hour_csv['Type'] = hour['type']
                hour_csv['Monday'] = hour['timings'].get('Monday', '')
                hour_csv['Tuesday'] = hour['timings'].get('Tuesday', '')
                hour_csv['Wednesday'] = hour['timings'].get('Wednesday', '')
                hour_csv['Thursday'] = hour['timings'].get('Thursday', '')
                hour_csv['Friday'] = hour['timings'].get('Friday', '')
                hour_csv['Saturday'] = hour['timings'].get('Saturday', '')
                hour_csv['Sunday'] = hour['timings'].get('Sunday', '')
                yield hour_csv
            
            yield more

            self.logger.info(f"Scraped Resturant: {resturant['name']}")
        except Exception as e:
            print('parse_images',e)


    def closed(self, reason):
        with open('Cities_with_no_record.csv', 'w', newline='') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerows(self.unfound_locations)

        moreData = json.load(open(MENU_FILENAME))
        with open(MENU_FILENAME, 'w') as f:
            json.dump(moreData, f, indent=4)