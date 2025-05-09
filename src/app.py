"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_members():
    # This is how you can use the Family datastructure by calling its methods
    try:
        response_body = jackson_family.get_all_members()
        return jsonify(response_body), 200
    except:
        return "Server error", 500

@app.route ('/members/<int:id>', methods= ['GET'])
def handle_member(id):
    try:
        response_body = jackson_family.get_member(id)
        if response_body == "Not found":
            return jsonify("Member Id not found"), 400
        return jsonify(response_body), 200
    except:
        return "Server error", 500

@app.route('/members', methods= ['POST'])
def handle_new_member():
    try:
        request_body = request.json
        print(request_body.keys())
        if "first_name" not in request_body.keys() or "age" not in request_body.keys() or "lucky_numbers" not in request_body.keys():
            return jsonify("Wrong family member format"), 400
        response_body= jackson_family.add_member(request_body)
        return jsonify(response_body), 200
    except:
        return "Server error", 500


@app.route('/members/<int:member_id>', methods= ['DELETE'])
def handle_delete_member(member_id):
    try:
        response_body = jackson_family.delete_member(member_id)
        if response_body ==  "Member not found":
            return jsonify({"done":False}), 400
        return jsonify({"done":True}), 200
    except:
        return "Server error", 500

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
