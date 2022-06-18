from flask import Flask, jsonify, make_response

from flask_restx import Api, Resource
from utils.fetchData import isAlreadyCheckIn
from utils.fetchData import checkIn

app = Flask(__name__)
api = Api(app)


@api.route('/checkin/<string:user>')
class Hello(Resource):
  def get(self, user):
    try:
      alreadyCheckIn = isAlreadyCheckIn(user)
    except:
      return make_response(jsonify({'error': 'User Not Found'}), 404)

    if alreadyCheckIn:
      return make_response(jsonify({'error': 'Already Check In'}), 409)

    try:
      checkIn(user)
    except:
      return make_response(jsonify({'error': 'Database Not Found'}), 404)

    return make_response(jsonify({'Status': 'OK'}), 200)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
