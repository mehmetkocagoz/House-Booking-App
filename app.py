from flask import Flask,request,jsonify,Response
from db import getHouses, getHousesWithCity
import json

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello From Flask!"


@app.route('/houses')
def all_houses():
    
    houses_data = getHouses()

    if houses_data is not None:
        response_data = {'houses': houses_data}
    else:
        response_data = {'error': 'Failed to fetch houses data'}
    
    # Manually creating the JSON-formatted string
    json_response = json.dumps(response_data, indent=2)
    # Returning the response as JSON
    return Response(json_response, content_type='application/json; charset=utf-8')

@app.route('/houseswithquery')
def houses_with_query():
    city = request.args.get('city')
    date_from = request.args.get('datefrom')
    date_to = request.args.get('dateto')
    number_of_peoples = request.args.get('numberofpeople')

    # Set default values for pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    house_list_for_given_city = getHousesWithCity(city)

    total_house_count = len(house_list_for_given_city)
    total_pages = (total_house_count + per_page - 1) // per_page

    start_index = (page - 1) * per_page
    end_index = min(page * per_page, total_house_count)

    house_list_for_given_page = house_list_for_given_city[start_index:end_index]
     # Construct the final response
    response_data = {
        'houses': house_list_for_given_page,
        'pageNumber': page,
        'totalPages': total_pages
    }

    return Response(json.dumps(response_data,indent=2),content_type='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run()
