import datetime
import re
import requests
from .settings import USER_AGENT


headers = {
    'user-agent': USER_AGENT
}


def get_menu(menuData):
    '''
        Parses menu data
    '''
    menus = []
    for type_ in menuData:
        t = {}
        t['menuType'] = get_value(type_,['title'])
        t['description'] = get_value(type_, ['description'])
        t['sections'] = []
        for sec in type_.get('sections', []):
            s = {}
            s['sectionType'] = get_value(sec, ['title'])
            s['description'] = get_value(sec, ['description'])
            s['items'] = []
            for item in sec.get('items', []):
                i = {}
                i['title'] = get_value(item, ['title'])
                i['description'] = get_value(item, ['description'])
                price = get_value(item, ['price'])
                i['price'] = '$' + str(price) if price else ''
                s['items'].append(i)
            t['sections'].append(s)
        menus.append(t)

    return menus


def expand_week(weeks):
    all_weeks = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    weeks_ff = {'mon' : 'Monday', 'tue' : 'Tuesday', 'wed' : 'Wednesday','thu' : 'Thursday', 
                'fri' : 'Friday', 'sat' : 'Saturday', 'sun' : 'Sunday'}
    
    weeks = weeks.lower().strip()
    if weeks == 'daily':
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    se = weeks.split('–')
    se = [s.strip() for s in se]

    expanded_weeks = []
    if len(se) > 1:
        start = se[0]
        end = se[1]
        expanded_weeks = all_weeks[all_weeks.index(start) : all_weeks.index(end)+1]
    else:
        expanded_weeks = [se[0]]
    

    expanded_weeks = [weeks_ff[e] for e in expanded_weeks]
    return expanded_weeks

def parse_timings(txts):
    week_timings = {
        'Monday' : [],
        'Tuesday' : [],
        'Wednesday' : [],
        'Thursday' : [],
        'Friday' : [],
        'Saturday' : [],
        'Sunday' : [],
    }
    
    for txt in txts:
        time_ptrn = r'([0-1]?[0-9]|2[0-3]):[0-5][0-9] *[AaPp][Mm]'

        timings = []
        for m in re.finditer(time_ptrn, txt):
             timings.append(txt[m.start() : m.end()])

        timings = ' - '.join([t.replace(' ','') for t in timings])

        weeks = re.split(time_ptrn, txt)[0].strip()
        weeks = weeks.split(',')

        for w in weeks:
            for day in expand_week(w):
                week_timings[day].append(timings)
    
    for k, v in week_timings.items():
        week_timings[k] = '; '.join(v)
    
    return week_timings

def parse_hours(data):
    data = data.replace('â\x80\x93', '-').replace('<br />','')
    data = data.split('\n')

    week_keywords = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'daily']

    records = {}
    current_key = 'Default'
    for row in data:
        row = row.strip()
        check_row = row.lower().replace('–',' ').split()
        if not any(key in check_row for key in week_keywords):
            current_key = row
        else:
            record = records.get(current_key, [])
            record.append(row)
            records[current_key] = record
        
    hours = []
    for k, v in records.items():
        hour= {}
        hour['type'] = k
        hour['timings'] = parse_timings(v)
        hours.append(hour)
    return hours





def get_auto_sha():
    try:
        url = 'https://www.opentable.com'
        text = requests.get(url, headers=headers, timeout=30).text
        js_url = re.findall(r'//cdn.otstatic.com/cfe/.+/js/home-.*\.js', text)
        if js_url:
            js_url = 'https:' + js_url[0]
            
            res = requests.get(js_url, timeout=10)
            cdn_urls = re.findall(r'"js/".*{(.*)}.*".chunk.js"', res.text)[0].split(',')
            cdn_urls = [c.replace(':','-').replace('"','') for c in cdn_urls]
            
            base_url = js_url.rsplit('/',1)[0]
            for url in cdn_urls:
                url = base_url + f'/{url}.chunk.js'
                res = requests.get(url, timeout=10)

                start = res.text.find('"Autocomplete")')
                a = res.text.find('=',start)
                z = res.text.find('"',a+5)
                sha = res.text[a:z]
                if sha:
                    return sha.replace('"','').replace('=','')
    except:
        pass
    return '3cabca79abcb0db395d3cbebb4d47d41f3ddd69442eba3a57f76b943cceb8cf4'


def get_multi_sha():
    try:
        url = 'https://www.opentable.com/s'
        text = requests.get(url, headers=headers, timeout=30).text
        js_url = re.findall(r'//cdn.otstatic.com/cfe/.+/js/multi-search-.*\.js', text)

        if js_url:
            js_url = 'https:' + js_url[0]
            
            res = requests.get(js_url, timeout=10)
            start = res.text.find('"RestaurantFieldsMultiSearch")')
            a = res.text.find('=',start)
            z = res.text.find('"',a+5)
            sha = res.text[a:z]
            if sha:
                return sha.replace('"','').replace('=','')
    except:
        pass
    return '8206555682d1001110601b6cd2660625248e6e9db3e784f3e1ca73019680a007'


def get_photo_sha():
    try:
        url = 'https://www.opentable.com/r/nido-austin'
        text = requests.get(url, headers=headers, timeout=30).text
        js_url = re.findall(r'//cdn.otstatic.com/cfe/.+/js/restprofilepage-.*\.js', text)
     
        if js_url:
            js_url = 'https:' + js_url[0]
            
            res = requests.get(js_url, timeout=10)
            start = res.text.find('"photoGallery")')
            a = res.text.find('=',start)
            z = res.text.find('"',a+5)
            sha = res.text[a:z]
            if sha:
                return sha.replace('"','').replace('=','')
    except:
        pass
    return '2b9a865b5c475d34dac5b1fe4350abd97a513b9d8d1b93d58f46b01b53d28dbe'


def get_value(field, keys):
    try:
        for key in keys:
            field = field[key]
        if field:
            return field
    except:
        pass
    return ''






def get_images(images):
    results = {
        'food' : [],
        'drinks' : [],
        'interior' : [],
        'exterior' : []
    }

    nfood, ndrinks, ninside, noutside = 0, 0, 0, 0
    for image in images:
        if image['category'] == 'food' and nfood < 5:
            for photo in image['thumbnails']:
                if photo['label'] == 'large':
                    nfood += 1
                    results['food'].append(photo['url'])

        elif image['category'] == 'drink' and ndrinks < 5:
            for photo in image['thumbnails']:
                if photo['label'] == 'large':
                    ndrinks += 1
                    results['drinks'].append(photo['url'])

        elif image['category'] == 'interior' and ninside < 5:
            for photo in image['thumbnails']:
                if photo['label'] == 'large':
                    ninside += 1
                    results['interior'].append(photo['url'])

        elif image['category'] == 'exterior' and noutside < 5:
            for photo in image['thumbnails']:
                if photo['label'] == 'large':
                    noutside += 1
                    results['exterior'].append(photo['url'])

    return results              

def get_city_data(term, auto_sha):
    return {
            "operationName": "Autocomplete",
            "variables": {
                "term": term,
                "latitude": 1,
                "longitude": -1,
                "useNewVersion": True
            },
            "extensions": {
                "persistedQuery": {
                "version": 1,
                "sha256Hash": auto_sha
                }
            }
        }


def get_image_data(id, photo_sha):
    return {
            "operationName": "photoGallery",
            "variables": {
                "restaurantId": id,
                "pageSize": 10000,
                "pageNumber": 1,
                "instagramOptOut": True,
                "includeProfile": True,
                "includeGooglePhotos": True,
            },
            "extensions": {
                "persistedQuery": {
                "version": 1,
                "sha256Hash": photo_sha
                }
            }
        }

def get_multisearch_data(metro_id, multi_sha):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    return {
                        "operationName": "MultiSearchRestaurants",
                        "variables": {
                            "limit": 10000,
                            "popLimit": 3,
                            "skipResults": 0,
                            "skipPopResults": 9,
                            "diningType": "ALL",
                            "sortBy": "WEB_CONVERSION",
                            "mods": [
                            "NO_INCENTIVE_PROMOTION"
                            ],
                            "withAnytimeAvailability": True,
                            "forwardMinutes": 150,
                            "backwardMinutes": 150,
                            "notWithAnytimeAvailability": False,
                            "notWithFacets": False,
                            "needRemodeledSearchFacets": True,
                            "withFallbackToListingMode": False,
                            "proofOfVaccinationRequired": False,
                            "onlyWithOffers": False,
                            "isAffiliateSearch": False,
                            "groupsRids": False,
                            "metroId": metro_id,
                            "macroIds": [],
                            "legacyHoodIds": [],
                            "tld": "com",
                            "date": today,
                            "time": "19:00",
                            "partySize": 2,
                            "prices": [],
                            "cuisineIds": [],
                            "tagIds": [],
                            "tableCategories": [],
                            "onlyPop": False,
                            "includePopRestaurants": False,
                            "pinnedRid": None,
                            "shouldIncludeDeliveryDetails": True,
                            "shouldIncludeTakeoutDetails": True,
                            "loyaltyRedemptionTiers": [],
                            "additionalDetailIds": [],
                            "experienceTypeIds": [],
                            "dniTagIds": [],
                            "device": "desktop",
                            "debug": False,
                            "withFacets": False,
                            "withTags": True,
                            "withLoyaltyRedemptionFacets": False,
                            "withPointRedemptionRewards": False,
                            "countryCode": "US"
                        },
                        "extensions": {
                            "persistedQuery": {
                            "version": 1,
                            "sha256Hash": multi_sha
                            }
                        }
                    }
