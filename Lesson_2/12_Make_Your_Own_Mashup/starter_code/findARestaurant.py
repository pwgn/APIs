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
    print 'Request:', mealType, location

	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    lat, lng = getGeocodeLocation(location)
    print 'Geo location:', lat, lng

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    restaurants = findNearbyRestaurants(mealType, lat, lng)

	#3. Grab the first restaurant
    restaurant = restaurants['venues'][0]

	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    restaurant_img_url = getRestaurantImageUrl(restaurant['id'])

	#5. Grab the first image
	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url

def findNearbyRestaurants(mealType, lat, lng):
    url = ('https://api.foursquare.com/v2/venues/search?ll=%s,%s&query=%s&v=%s&client_id=%s&client_secret=%s'%
               (lat, lng, mealType, foursquare_version, foursquare_client_id, foursquare_client_secret))

    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    print 'Url:', url
    return result['response']

def getRestaurantImageUrl(venue_id):
    img_size = '300x300'
    url = ('https://api.foursquare.com/v2/venues/%s/photos?&v=%s&client_id=%s&client_secret=%s'% (venue_id, foursquare_version, foursquare_client_id, foursquare_client_secret))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    photos = result['response']['photos']

    # Default image
    image_url = 'http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct'

    # Set restaurant image
    if photos['count'] > 0:
        image = photos['items'][0]
        image_url = image['prefix'] + '300x300' + image['suffix']

    print 'Image url:', image_url
    return result

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
