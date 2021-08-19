from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from code.models.item_model import ItemModel
from code.models.store_model import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": f"Store {name} cannot be found."}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"Store {name} already exists"}, 400

        store = StoreModel(name)
        try:
            store.save_store_to_db()
        except:
            return {f"message": "Error inserting item {name}"}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_item_from_db()
        return {"message": f"Store {name} deleted"}, 201


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}, 200
