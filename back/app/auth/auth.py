from flask import g
from app import mongo, serializer
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.get_password
def get_password(userName):
    user = mongo.db.users.find_one({'name': userName})
    if not user:
        return None
    g.user = user['name']
    #g.user_id = mongo.db.users.find_one({'name': g.user})['_id']
    return user['pwd']


@token_auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        #g.user_id = mongo.db.users.find_one({'name': g.user})['_id']
        return True
    return False
