from .auth.auth import AuthError, requires_permissions
from .database.models import setup_db, db_drop_and_create_all, Drink
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
import os
from sqlalchemy import exc
import sys

app = Flask(__name__)
with app.app_context():
    setup_db(app)
    db_drop_and_create_all()

CORS(app)


# ROUTES
@app.route("/drinks")
def get_drinks():
    drinks = Drink.query.all()

    # format
    formatted_drinks = [drink.short() for drink in drinks]

    return jsonify({"succes": True, "drinks": formatted_drinks}), 200


@app.route("/drinks-detail")
@requires_permissions("get:drinks-detail")
def get_drinks_detail(payload):
    drinks = Drink.query.all()

    # format
    formatted_drinks = [drink.long() for drink in drinks]

    return jsonify({"succes": True, "drinks": formatted_drinks}), 200


@app.route("/drinks", methods=["POST"])
@requires_permissions("post:drinks")
def post_drinks(payload):
    # Grab JSON
    try:
        title, recipe = (request.json["title"], request.json["recipe"])

    except KeyError:
        abort(400)

    try:
        new_drink = Drink(title=title, recipe=json.dumps([recipe]))
        new_drink.insert()

    except:
        print(sys.exc_info())
        abort(500)

    return jsonify({"success": True, "drinks": [new_drink.long()]}), 200


@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_permissions("patch:drinks")
def patch_drink(payload, drink_id):
    # get existing model
    drink = Drink.query.get(drink_id)

    if not drink:
        abort(404)

    # Parse the PATCH request data
    data = request.get_json()

    # Update the attributes of the existing object with the new data
    try:
        for key, value in data.items():
            setattr(drink, key, value)
    except:
        abort(400)

    try:
        drink.update()
    except:
        abort(422)

    return jsonify({"success": True, "drinks": [drink.long()]}), 200


@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_permissions("delete:drinks")
def delete_drinks(payload, drink_id):
    # get drink
    drink = Drink.query.get(drink_id)

    if not drink:
        abort(404)

    try:
        drink.delete()
    except:
        abort(500)

    return jsonify({"success": True, "delete": drink.id})


# Error handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400


@app.errorhandler(401)
def bad_request(error):
    return jsonify({"success": False, "error": 401, "message": "Unauthorised"}), 401


@app.errorhandler(403)
def bad_request(error):
    return jsonify({"success": False, "error": 403, "message": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "Unprocessable"}), 422


@app.errorhandler(500)
def server_error(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 500,
                "message": "Server error",
            }
        ),
        500,
    )


if __name__ == "__main__":
    app.run()
