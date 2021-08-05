import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import sys
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.app import AuthError, requires_auth

app = Flask(__name__, instance_relative_config=True)
setup_db(app)
CORS(app)


# db_drop_and_create_all()


@app.route('/drinks', methods=['GET'])
def getDrinks():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def getDrinkdetails():
    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def postDrink(payload):
    req = request.get_json()

    try:
        req = req['recipe']
        if isinstance(req, dict):
            req = [req]

        drink = Drink()
        drink.title = req['title']
        drink.recipe = json.dumps(req)
        drink.insert()

    except BaseException:
        abort(400)

    return jsonify({'success': True, 'drinks': [drink.long()]})



@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def PATCH_drink(payload, id):
    req = request.get_json()
    drink = Drink.query.filter(Drink.id == id).all()

    if not drink:
        abort(404)

    try:
        title = req.get('title')
        recipe = req.get('recipe')
        if title:
            drink.title = title

        if recipe:
            drink.recipe = json.dumps(req['recipe'])

        drink.update()
    except BaseException:
        abort(400)

    return jsonify({'success': True, 'drinks': [drink.long()]}), 200



@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleteDrink(id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if not drink:
        abort(404)
    try:
        drink.delete()
    except BaseException:
        abort(400)

    return jsonify({'success': True, 'delete': id}), 200



@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422



@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400