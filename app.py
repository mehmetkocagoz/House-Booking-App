from flask import Flask,request,jsonify,Response,send_from_directory
from db import getHouses, getHousesWithCity,checkUser
import json
import jwt
from datetime import datetime,timedelta
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'examplesecretkey'

@app.route('/')
def home():
    return "Hello From Flask!"

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : 'Flask API'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired!'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'Alert!': f'Invalid Token: {str(e)}'}), 401
        return func(*args, **kwargs)
    return decorated


@app.route('/login', methods=['POST'])
def login_post():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract username and password from the JSON data
        username = data.get('username')
        password = data.get('password')

        # Validate the credentials
        if checkUser(username,password):
            # Successful login
            token = jwt.encode({
                'user':username,
                'expiration': str(datetime.utcnow() + timedelta(seconds=240))
            },
            app.config['SECRET_KEY'])
            decoded_token = token
            response_data = {'message': 'Login successful','Token': decoded_token}
            return jsonify(response_data), 200
        else:
            # Failed login
            response_data = {'error': 'Invalid credentials'}
            return jsonify(response_data), 401

    except Exception as e:
        # Handle exceptions or errors
        return jsonify({'error': str(e)}), 400


@app.route('/houses')
@token_required
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
