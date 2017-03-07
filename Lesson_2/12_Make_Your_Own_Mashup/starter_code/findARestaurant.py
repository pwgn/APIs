from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
from pprint import pprint as pp
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "PASTE_YOUR_ID_HERE"
foursquare_client_secret = "YOUR_SECRET_HERE"
foursquare_version = '20170101'


def findARestaurant(mealType,location):
    print
    print
    print 'Request:', mealType, location
    print
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    lat, lng = getGeocodeLocation(location)

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    restaurants = findNearbyRestaurants(mealType, lat, lng)

	#3. Grab the first restaurant
    if not restaurants['venues']:
        return 'No restaurants found'

    restaurant = restaurants['venues'][0]

	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    restaurant_photos = getRestaurantImageUrl(restaurant['id'])

	#5. Grab the first image
	#6. If no image is available, insert default a image url
    # Default image
    image_url = 'http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct'

    # Set restaurant image
    if restaurant_photos['count'] > 0:
        image = restaurant_photos['items'][0]
        image_url = image['prefix'] + '300x300' + image['suffix']

	#7. Return a dictionary containing the restaurant name, address, and image url
    print 'Restaurant Name:', restaurant['name']
    print 'Restaurant Address:', ', '.join(restaurant['location']['formattedAddress'])
    print 'Image:', image_url

def findNearbyRestaurants(mealType, lat, lng):
    url = appendForesquareAuthParameters(('https://api.foursquare.com/v2/venues/search?ll=%s,%s&query=%s'%
               (lat, lng, mealType)))

    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    return result['response']

def getRestaurantImageUrl(venue_id):
    img_size = '300x300'
    url = appendForesquareAuthParameters('https://api.foursquare.com/v2/venues/%s/photos?'% (venue_id))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    photos = result['response']['photos']

    return photos


def appendForesquareAuthParameters(url):
    auth_url = (url + '&v=%s&client_id=%s&client_secret=%s'%
                    (foursquare_version, foursquare_client_id, foursquare_client_secret))

    return auth_url

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
