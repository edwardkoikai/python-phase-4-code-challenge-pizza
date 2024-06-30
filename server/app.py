#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants')
def restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        # restaurant_dict = restaurant.to_dict()
        restaurant_dict = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }
        restaurants.append(restaurant_dict)
        
    response = make_response(
        restaurants,
        200
    )
    
    return response
    
@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant =Restaurant.query.filter(Restaurant.id ==id).first()
    
    if request.method == 'GET':
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            response_body = restaurant_dict
            status = 200
        else:
            response_body = {
                "error": "Restaurant not found"
            }
            status = 404
        return make_response(response_body, status)
    
    elif request.method == 'DELETE':
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            response_body = {
                'delete_successful': True,
                "message": "Restaurant deleted"
            }
            status = 204
        else:
            response_body = {
                "error": "Restaurant not found"
            }
            status = 401
            
        response = make_response(response_body, status)
        return response
        
@app.route('/pizzas')
def pizzas():
    pizzas = [] 
    
    for pizza in Pizza.query.all():
        pizza_dict = {
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name
        }
        pizzas.append(pizza_dict)
        
    response = make_response(
        pizzas, 
        200
    )
    
    return response
        
        

    


if __name__ == "__main__":
    app.run(port=5555, debug=True)
