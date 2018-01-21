from flask import Flask, render_template, request
import urllib.request, json
from datetime import datetime, timedelta
from math import radians, sin, cos, acos, atan2, sqrt, degrees
from operator import methodcaller



app = Flask(__name__)
#new_places_dictionary 
#places_on_route 
#API Key = GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx
#client ID = OkyFz7f00cpLklJ7lzfEHg

class Place:
	def __init__(self, name, lat, lon, rating):
		self.name = name
		self.latitude = lat
		self.longitude = lon
		self.rating = rating
		self.has_rating = False
		self.review_num = 0
		self.image = ""
		self.url = ""
	
	def get_name(self):
		return self.name;
	
	def get_latitude(self):
		return self.latitude
	
	def get_longitude(self):
		return self.longitude
	
	def get_rating(self):
		return self.rating

	def set_rating(self, rating):
		self.rating = rating
		self.has_rating = True

	def get_url(self):
		return self.url

	def set_url(self, url):
		self.url = url

	def get_review_num(self):
		return self.review_num

	def set_review_num(self, review_num):
		self.review_num = review_num

	def get_image(self):
		return self.image

	def set_image(self, image):
		self.image = image


	def get_distance(self, destination):
		starting_latitude = radians(float(self.latitude))
		ending_latitude = radians(float(destination.get_latitude()))
		starting_longitude = radians(float(self.longitude))
		ending_longitude = radians(float(destination.get_longitude()))
		return 6371.01 * acos(sin(starting_latitude) * sin(ending_latitude) + cos(starting_latitude) * cos(ending_latitude) * cos(starting_longitude - ending_longitude))

	def get_has_rating(self):
		return self.has_rating

class Relation:
	def __init__(self, start, destination):
		self.start = start
		self.destination = destination

		endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
		api_key = 'AIzaSyC-g2jSdIeWUogOM5Kvs5D1wFAJ5ePDvcs'
		#Asks the user to input Where they are and where they want to go.
		origin = start.replace(' ','+')
		destination = destination.replace(' ','+')
		#Building the URL for the request
		nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
		request = endpoint + nav_request
		#Sends the request and reads the response.
		response = urllib.request.urlopen(request).read()
		#Loads response as JSON
		directions = json.loads(response)
		info = directions['routes'][0]['legs'][0]


		self.start_location_lat = info['start_location']['lat']
		self.start_location_lng = info['start_location']['lng']
		self.end_location_lat = info['end_location']['lat']
		self.end_location_lng = info['end_location']['lng']
		#duration in minutes
		self.duration = info['duration']['value']/60 
		#distance in meters
		self.distance = info['distance']['value']
		#all steps
		self.steps = info['steps']

		print(self.duration)
		print(self.distance)
		print(len(self.steps))



	def get_distance(self):
		return self.duration

	def get_duration(self):
		return self.duration

	#Finds approximately what latitude,longitude we will be at during the time to eat
	def get_location_at_time(self, timetoeat):
		now = datetime.now()
		diff = timedelta(hours=24) - (now - now.replace(hour=timetoeat.hour, minute=timetoeat.minute, second=timetoeat.second, microsecond=0))
		diff = (diff.total_seconds() % (24 * 3600))/60
		if (duration < diff):
			return self.end_location, self.end_location_lng
		else:
			while 

		
		curr_location_lat = self.start_location_lat
		curr_location_lng = self.start_location_lng












def query_header_constructor(query, at_bool, at_val, in_val):
	"""Generates a dictionary named headers which stores a common set of parameters for the get requests in search_query, autosuggest_query, and explore_query"""
	APP_ID = "JlpRxY5ZfJmmqFMIoiGe"
	APP_CODE = "_0Wcx47HZmzeB48BpMHGGg"
	headers = dict()
	headers["app_id"] = APP_ID
	headers["app_code"] = APP_CODE
	if query is not None:
		headers["q"] = query
	if at_bool:
		headers["at"] = at_val
	# else:
	# 	headers["in"] = in_val
	return headers

def places_lst_constructor(results, number_of_places):
	"""Takes in the results of a previous query and returns a list of Places with a size equal to the number of places requested"""
	places = []
	for x in range(0, number_of_places):
		target_place = results[x]
		rating = None
		if "averageRating" in target_place:
			rating = target_place.get("averageRating")
		places.append(Place(target_place["title"], target_place["position"][0], target_place["position"][1], rating))
	return places

#fixing route
def search_query(query, number_of_places, at_bool, at_val, in_val, lat1, lon1, lat2, lon2):
	"""Does a search query(Nokia Here Places API) and returns a list of places"""
	url = query_url_constructor("/discover/search")
	headers = query_header_constructor(query, at_bool, at_val, in_val)
	headers["route"] = "[" + str(lat1) + "," + str(lon1) + "|" + str(lat2) + "," + str(lon2) + "];w=100000" 
	r = requests.get(url, params=headers)
	s = json.loads(r.text)
	results = s["results"]
	results = results["items"]
	return places_lst_constructor(results, number_of_places)


place1 = Place("Seattle", 47.608013, -122.335167, None)
place2 = Place("San Francisco", 37.773972, -122.431297, None)
place3 = Place("Los Angeles", 34.052235, -118.243683, None)

#Test for four_category_lists
# lst = search_query("Museum", 3, False, "47.608013,-122.335167", center_circle_constructor(place2, place1), 37.773972, -122.431297, 34.052235, -118.243683)
# for x in range(0,3):
# 	print(lst[x].get_name())

# lst = search_query("Museum", 3, False, "47.608013,-122.335167", center_circle_constructor(place2, place1))
# for x in range(0,3):
# 	print(lst[x].get_name())


def four_category_lists(choices_list, number_of_places, at_bool, at_val, starting_place, destination):
	for category in choices_list:
		lst = search_query(category, number_of_places, at_bool, at_val, center_circle_constructor(starting_place, destination))
		for x in range(0, number_of_places):
			print(lst[x].get_name())


def yelp_api_set_rating_url_review_text(term, latitude, longitude, place):
	#API Key = GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx
	url = "https://api.yelp.com/v3/businesses/search"
	headers = {
        'Authorization': 'Bearer GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx',
	}
	url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'limit': 10
    }
	response = requests.request('GET', url, headers=headers, params=url_params)
	s = json.loads(response.text)
	for p in s['businesses']:
		if p['name'] == term:
			place.set_rating(p['rating'])
			place.set_url(p['url'])
			place.set_image(p['image_url'])
			place.set_review_num(p['review_count'])
			return
	place.set_rating(0)
	place.set_url("")
	place.set_image("")
	place.set_review_num(0)
	return

def yelp_api_set_rating(term, latitude, longitude):
	#uses yelp api to get a place's rating
	url = "https://api.yelp.com/v3/businesses/search"
	headers = {
        'Authorization': 'Bearer GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx',
	}
	url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'limit': 10
    }
	response = requests.request('GET', url, headers=headers, params=url_params)
	s = json.loads(response.text)
	for place in s['businesses']:
		if place['name'] == term:
			rating = place['rating']
			return rating
	return "Place has no rating"
def star_url(number_of_stars):
	star_path = "/static/yelp_stars/web_and_ios/large/"
	if number_of_stars == 0:
		star_path += "large_0.png"
	elif number_of_stars == 1:
		star_path += "large_1.png"
	elif number_of_stars == 2:
		star_path += "large_2.png"
	elif number_of_stars == 3:
		star_path += "large_3.png"
	elif number_of_stars == 4:
		star_path += "large_4.png"
	elif number_of_stars == 5:
		star_path += "large_5.png"
	elif number_of_stars == 1.5:
		star_path += "large_1_half.png"
	elif number_of_stars == 2.5:
		star_path += "large_2_half.png"
	elif number_of_stars == 3.5:
		star_path += "large_3_half.png"
	else:
		star_path += "large_4_half.png"
	return star_path

#ranks places to visit based on ratings
def place_ranker(lst_places):
	new_lst = sorted(lst_places, key=methodcaller('get_rating'))[::-1]
	to_return = []
	for place in new_lst:
		to_return.append(place.get_name())
	return to_return

@app.route('/')
def welcome_to_food_stop():
    return render_template('startingtrip.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
    global place_relation
    start = request.form['place1']
    destination = request.form['place2']
    strtime = request.form['timetoeat']
    timetoeat = datetime.strptime(strtime, '%H:%M').time()

    place_relation = Relation(start, destination)
    eat_lat, eat_long = place_relation.get_location_at_time(timetoeat)

    place_lst = search_query("Museum", 5, False, "47.608013,-122.335167", "", 37.773972, -122.431297, 34.052235, -118.243683)
    for place in place_lst:
    	yelp_api_set_rating_url_review_text(place.get_name(), place.get_latitude(), place.get_longitude(), place)
    place_ranker(place_lst)
    return render_template(
    'submittedform.html',
    place1=place1,
    place2=place2,
    timetoeat=strtime
    )
@app.route('/mapinterface', methods=['POST'])
def first_map():
	# lst = here.search_query(x,x,x,x)
	#make dict out of list
	#take first 5
    global place_lst
    print(place_lst)
    place1 = place_lst[0]
    place2 = place_lst[1]
    place3 = place_lst[2]
    place4 = place_lst[3]
    place5 = place_lst[4]
    place1_name = place1.get_name()
    place2_name = place2.get_name()
    place3_name = place3.get_name()
    place4_name = place4.get_name()
    place5_name = place5.get_name()
    place1_image = place1.get_image()
    place2_image = place2.get_image()
    place3_image = place3.get_image()
    place4_image = place4.get_image()
    place5_image = place5.get_image()
    place1_review_num = place1.get_review_num()
    place2_review_num = place2.get_review_num()
    place3_review_num = place3.get_review_num()
    place4_review_num = place4.get_review_num()
    place5_review_num = place5.get_review_num()
    place1_rating = place1.get_rating()
    place2_rating = place2.get_rating()
    place3_rating = place3.get_rating()
    place4_rating = place4.get_rating()
    place5_rating = place5.get_rating()
    place1_url = place1.get_url()
    place2_url = place2.get_url()
    place3_url = place3.get_url()
    place4_url = place4.get_url()
    place5_url = place5.get_url()
    place1_stars = star_url(place1_rating)
    place2_stars = star_url(place2_rating)
    place3_stars = star_url(place3_rating)
    place4_stars = star_url(place4_rating)
    place5_stars = star_url(place5_rating)


    return render_template('mapinterface.html',
    place1_name = place1_name,
    place2_name = place2_name,
    place3_name = place3_name,
    place4_name = place4_name,
    place5_name = place5_name,
    place1_image = place1_image,
    place2_image = place2_image,
    place3_image = place3_image,
    place4_image = place4_image,
    place5_image = place5_image,
    place1_review_num = place1_review_num,
    place2_review_num = place2_review_num,
    place3_review_num = place3_review_num,
    place4_review_num = place4_review_num,
    place5_review_num = place5_review_num,
    place1_url = place1_url,
    place2_url =  place2_url,
    place3_url = place3_url,
    place4_url = place4_url,
    place5_url = place5_url,
    place1_stars = place1_stars,
    place2_stars = place2_stars,
    place3_stars = place3_stars,
    place4_stars = place4_stars,
    place5_stars = place5_stars
    )