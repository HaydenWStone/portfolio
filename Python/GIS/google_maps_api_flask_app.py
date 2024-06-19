
from flask import Flask, render_template, request
import requests
from math import radians, sin, cos, sqrt, atan2
import os

app = Flask(__name__)

api_key = os.environ.get('API_KEY')
min_rating = 4.5
radius = 5000

def geocoder(address):
    response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}')
    if response.status_code == 200:
        data = response.json()
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        location = f"{latitude},{longitude}"
        return location, latitude, longitude
    else:
        return None, None, None

def get_places(address, food):
    location, latitude, longitude = geocoder(address)
    if not location:
        return []

    response = requests.get(
        f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={food}&opennow=true&key={api_key}')
    if response.status_code == 200:
        data = response.json()
        places = data['results']
        filtered_places = [p for p in places if 'rating' in p and p['rating'] >= min_rating and (
                'bar' in p['types'] or 'restaurant' in p['types'] or 'cafe' in p['types'] or 'bakery' in p['types'])]
        sorted_places = sorted(filtered_places, key=lambda p: p['rating'], reverse=True)

        results = []
        for p in sorted_places:
            place_lat = radians(p['geometry']['location']['lat'])
            place_lng = radians(p['geometry']['location']['lng'])
            address_lat = radians(latitude)
            address_lng = radians(longitude)
            dlon = place_lng - address_lng
            dlat = place_lat - address_lat
            a = sin(dlat / 2) ** 2 + cos(address_lat) * cos(place_lat) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = 6371 * c * 0.621371

            place_id = p['place_id']
            details_response = requests.get(
                f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=url&key={api_key}')
            if details_response.status_code == 200:
                details_data = details_response.json()
                url = details_data['result']['url']
            else:
                url = ''

            results.append({
                'name': p['name'],
                'rating': p['rating'],
                'distance': distance,
                'vicinity': p['vicinity'],
                'url': url,
                'latitude': p['geometry']['location']['lat'],
                'longitude': p['geometry']['location']['lng']})

        return results
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        address = request.form.get('address')
        food = request.form.get('food')
        places = get_places(address, food)
        return render_template('results.html', api_key=api_key, places=places)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
