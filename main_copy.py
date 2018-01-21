from flask import Flask, render_template, request
import urllib.request, json
from datetime import datetime, timedelta
from operator import methodcaller



app = Flask(__name__)
#new_places_dictionary 
#places_on_route 
#API Key = GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx
#client ID = OkyFz7f00cpLklJ7lzfEHg

class Place:
	def __init__(self, name):
		self.name = name
		#self.lat = lat
		#self.lng = lng
		self.rating = None
		self.has_rating = False
		self.review_num = 0
		self.image = ""
		self.url = ""

	"""def __init__(self, name):
		self.name = name
		self.lat = None
		self.lng = None
		self.rating = None
		self.has_rating = False
		self.review_num = 0
		self.image = ""
		self.url = """""


	
	def get_name(self):
		return self.name;
	
	"""def get_latitude(self):
		return self.lat
	
	def get_longitude(self):
		return self.lng

	def set_latitude(self, lat):
		self.lat = lat
	
	def set_longitude(self, lng):
		self.lng = lng"""
	
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

	def get_has_rating(self):
		return self.has_rating

class Relation:
	def __init__(self, start, destination):
		self.start = start
		self.destination = destination

		endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
		api_key = 'AIzaSyC-g2jSdIeWUogOM5Kvs5D1wFAJ5ePDvcs'
		#Asks the user to input Where they are and where they want to go.
		origin = 'San Ramon'.replace(' ','+')
		end = 'San Jose'.replace(' ','+')
		#Building the URL for the request
		nav_request = 'origin={}&destination={}&key={}'.format(origin,end,api_key)
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
		#duration in seconds
		self.duration = info['duration']['value'] 
		#distance in meters
		self.distance = info['distance']['value']
		#all steps
		self.steps = info['steps']
		print('hello')


	def get_distance(self):
		return self.distance

	def get_duration(self):
		return self.duration

	def approx_location(self, curr_location_lat, curr_location_lng, next_location_lat, next_location_lng, step_duration, timetilleat):
		#fraction is the portion we completed of the step
		fraction = (timetilleat / step_duration)
		approx_location_lat = ((next_location_lat - curr_location_lat) * fraction) + curr_location_lat 
		approx_location_lng = ((next_location_lng - curr_location_lng) * fraction) + curr_location_lng
		return approx_location_lat, approx_location_lng



	#Finds approximately what latitude,longitude we will be at during the time to eat
	def get_location_at_time(self, timetoeat):
		now = datetime.now()
		timetilleat = timedelta(hours=24) - (now - now.replace(hour=timetoeat.hour, minute=timetoeat.minute, second=timetoeat.second, microsecond=0))
		timetilleat = timetilleat.total_seconds() % (24 * 3600)
		#if we reach the destination before timetoeat, we eat at the destination!
		if (self.duration <= timetilleat):
			return self.end_location_lat, self.end_location_lng
		else:
			curr_location_lat = self.start_location_lat
			curr_location_lng = self.start_location_lng
			for i in range(len(self.steps)):
				#if we won't make it to the next step, we need to eat food sometime in b/n step
				step_duration = self.steps[i]['duration']['value']
				next_location_lat = self.steps[i]['end_location']['lat']
				next_location_lng = self.steps[i]['end_location']['lng']
				if step_duration > timetilleat:
					return self.approx_location(curr_location_lat, curr_location_lng, next_location_lat, next_location_lng, step_duration, timetilleat)
				#go to next step!
				else:
					curr_location_lat = next_location_lat
					curr_location_lng = next_location_lng
					timetilleat -= step_duration

#place1 = Place("Seattle", 47.608013, -122.335167, None)
#place2 = Place("San Francisco", 37.773972, -122.431297, None)
#place3 = Place("Los Angeles", 34.052235, -118.243683, None)
def yelp_api_set_rating_url_review_text(timetoeat, lat, lng, n=5):
	#API Key = GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx
	url = "https://api.yelp.com/v3/businesses/search"
	headers = {
        'Authorization': 'Bearer GMeB-1KoNJ0XvhlOn9VFe4GPRCIWMusT-B-dwIYVSb0oG22RXFiUoBxz3gNvq4dTX2LenL6HWQwXoyLs9oJyFOIPWGFLRkPpKXo1KfCnENimVObU_vKl1clzLYZNWnYx',
	}
	url_params = {
        #'term': term.replace(' ', '+'),
        'categories': 'Restaurants',
        'latitude': lat,
        'longitude': lng,
        'sort_by': 'rating',
        #'open_at': timetoeat,
        'limit': n

    }
	response = requests.request('GET', url, headers=headers, params=url_params)
	s = json.loads(response.text)
	restaurant_list = []
	for r in s['businesses']:
		new_r = place(r['name'])
		new_r.set_rating(p['rating'])
		new_r.set_url(p['url'])
		new_r.set_image(p['image_url'])
		new_r.set_review_num(p['review_count'])
		restaurant_list.append(new_r)
	return restaurant_list

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


@app.route('/')
def welcome_to_food_stop():
    return render_template('startingtrip.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
	global place_lst
	start = request.form['start']
	destination = request.form['destination']
	strtime = request.form['timetoeat']
	timetoeat = datetime.strptime(strtime, '%H:%M').time()
	place_relation = Relation(start, destination)
	eat_lat, eat_lng = place_relation.get_location_at_time(timetoeat)
	place_lst = yelp_api_set_rating_url_review_text(timetoeat, eat_lat, eat_lng)
	return render_template(
    'submittedform.html',
    start=start,
    destination=destination,
    timetoeat=strtime
    )
@app.route('/mapinterface', methods=['POST'])
def first_map():
	# lst = here.search_query(x,x,x,x)
	#make dict out of list
	#take first 5
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