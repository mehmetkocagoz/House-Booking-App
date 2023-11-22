from flask import Flask,request,jsonify,Response
from db import getHouses
import json

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello From Flask!"


@app.route('/houses')
def houses():
    
    houses_data = getHouses()

    if houses_data is not None:
        response_data = {'houses': houses_data}
    else:
        response_data = {'error': 'Failed to fetch houses data'}
    
    # Manually creating the JSON-formatted string
    json_response = json.dumps(response_data, indent=2)
    # Returning the response as JSON
    return Response(json_response, content_type='application/json; charset=utf-8')


if __name__ == '__main__':
    app.run()
