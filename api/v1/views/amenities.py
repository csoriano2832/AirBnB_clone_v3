#!/usr/bin/python3
""" This module handles the HTTP methods of an amenity object"""
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

all_amenities = storage.all('Amenity')
amenities = []

for amenity in all_amenities.values():
    amenities.append(amenity.to_dict())


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """ Handles HTTP request of all the amenity objects """

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        amenity = Amenity(name=data.get('name'))
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """ Handles HTTP requests of a single state object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        data['id'] = amenity.id
        data['created_at'] = amenity.created_at
        amenity.__init__(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 200

    return jsonify(amenity.to_dict())
