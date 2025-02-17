"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    data = db.session.scalars(db.select(User)).all()
    result = list(map(lambda item: item.serialize(),data))

    if result == []:
        return jsonify({"msg":"there are no users"}), 404

    response_body = {
        "results": result
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    data = db.session.scalars(db.select(People)).all()
    result = list(map(lambda item: item.serialize(),data))

    if result == []:
        return jsonify({"msg":"there are no humanoid records"}), 404

    response_body = {
        "results": result
    }

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    try:
        people = db.session.execute(db.select(People).filter_by(id=people_id)).scalar_one()
        return jsonify({"result":people.serialize()}), 200
    except:
        return jsonify({"msg":"people do not exist"}), 404

@app.route('/planets', methods=['GET'])
def get_all_planets():
    data = db.session.scalars(db.select(Planets)).all()
    result = list(map(lambda item: item.serialize(),data))

    if result == []:
        return jsonify({"msg":"there are no existing planetary records"}), 404

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results": result
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    try:
        planets = db.session.execute(db.select(Planets).filter_by(id=planets_id)).scalar_one()
        return jsonify({"result":planets.serialize()}), 200
    except:
        return jsonify({"msg":"planet do not exist"}), 404
    
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    try:
        favorites = db.session.execute(db.select(Favorites).filter_by(user_id=user_id)).scalars().all()
        return jsonify({"result": [fav.serialize() for fav in favorites]}), 200

    except Exception as e:
        return jsonify({"msg":"Error", "error": str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
