from flask_restful import reqparse, abort, Api, Resource


# /api/users
class UserList(Resource):
    def get(self):
        '''유저 복수 조회'''
        pass
    
# /api/users/1
class User(Resource):
    def get(self, id):
        '''유저 단수 조회'''
        pass