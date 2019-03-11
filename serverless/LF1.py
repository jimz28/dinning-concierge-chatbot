import json
import datetime
import pprint
import time

from botocore.vendored import requests
from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
API_KEY = "qlLlM7QwWDc7AhJxLgIoX75UxfByp0s6cInxemyeLpefCD7w4yvpEyVRiXrjArD4gqOMHXH0k95T2YBrkFI7yUnYxclEiwmDC4XHqTNLlnahRgko8UYSFChAeXSEXHYx"
DEFAULT_TERM = 'dinner'

SEARCH_LIMIT = 3


def lambda_handler(event, context):
    name = str(event['currentIntent']['name'])
    print("name is " + name)
    msg = ""
    if name == "GreetingIntent":
        msg = "Hi,May I help you?"
    elif name == "Thanks":
        msg = "It's my pleasure!"
    elif name == "DiningSuggestion":
        date = event['currentIntent']['slots']['date']
        print("date is " + date)
        location = event['currentIntent']['slots']['City']
        print("location is " + location)
        cuisine = event['currentIntent']['slots']['cuisine']
        print("cuisine is " + cuisine);
        time = event['currentIntent']['slots']['time']
        print("time is " + time)
        number = event['currentIntent']['slots']['number']
        print("number is " + number)
        dateArr = []
        timeArr = []
        ans = {}
        dateArr = date.split("-")
        timeArr = time.split(":")
        dt = datetime.datetime(int(dateArr[0]),int(dateArr[1]),int(dateArr[2]),int(timeArr[0]),int(timeArr[1]))
        timeStamp = int("{:%s}".format(dt))
        print("timeStamp is " + str(timeStamp));
        ans = query_api(DEFAULT_TERM, location, cuisine)
        if bool(ans) == False :
            msg = "sorry ,no such restaurant in " + location + " on " + date + " at " + time
        else:
            msg = "Here are my " + cuisine +" restaurant suggestions for " + number+ " on " + date + " at " + time
            i = 1
            sug = ""
            for k,v in ans.items():
                sug += str(i) + ". " + k + " at " + str(v) + ". "
                i = i+1
            msg = msg + "\n"+ sug
    else:
        msg = "Opp! Wrong"

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": msg
              }
        }
    }
   
    return response;


def query_api(term, location, categories):
    response = search(API_KEY, term, location,categories)

    businesses = response.get('businesses')
    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = []
    for i in businesses:
        business_id.append(i['id'])

    #print(u'{0} businesses found, querying business info ' \
        #'for the top result "{1}" ...'.format(
            #len(businesses), business_id))
    response = get_business(API_KEY, business_id)
    
    return response
    
def search(api_key, term, location,categories):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'categories': categories.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)
    
    
    
def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()
    

def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    map = {};
    
    for i in range(3):
        business_path = BUSINESS_PATH + business_id[i]
        result = request(API_HOST, business_path, api_key)
        name = str(result['name'])
        print(name)
        addr = str(result['location']['address1'] + " " + result['location']['city'])
        print(addr)
        map[name] = addr
    return map
