#!/usr/bin/python3
""" This module handles the HTTP methods of a user object"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views

all_users = storage.all('User')
users = []

for user in all_users.values():
    users.append(user.to_dict())


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """ Handles HTTP request of all the user objects """

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        user = User(email=data.get('email'), password=data.get('password'))
        user.save()
        return jsonify(user.to_dict()), 201

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_user(user_id=None):
    """ Handles HTTP requests of a single user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        data['id'] = user.id
        data['email'] = user.email
        data['created_at'] = user.created_at
        user.__init__(**data)
        user.save()
        return jsonify(user.to_dict()), 200

    return jsonify(user.to_dict())
