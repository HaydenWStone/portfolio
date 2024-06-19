from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

def get_federal_land_info(longitude, latitude):
    url = "https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Federal_Lands/FeatureServer/0/query"
    params = {
        'f': 'json',
        'geometry': f'{longitude},{latitude}',
        'geometryType': 'esriGeometryPoint',
        'spatialRel': 'esriSpatialRelIntersects',
        'inSR': '4326',
        'outFields': 'Agency,unit_name,link',
        'returnGeometry': 'false'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if len(data['features']) > 0:
        feature = data['features'][0]['attributes']
        return {
            'on_federal_land': True,
            'agency': feature['Agency'],
            'unit_name': feature['unit_name'],
            'link_code': feature['link']
        }
    else:
        return {'on_federal_land': False}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_federal_land', methods=['GET'])
def check_federal_land():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    if not latitude or not longitude:
        return jsonify({'error': 'Missing latitude or longitude'}), 400

    land_info = get_federal_land_info(longitude, latitude)
    return jsonify(land_info)

if __name__ == '__main__':
    app.run(debug=True)
