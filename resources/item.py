from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from code.models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="The price cannot be left blank"
    )
    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="The store id cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": f"Item {name} cannot be found."}

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"Item {name} already exists"}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data)
        try:
            item.save_item_to_db()
        except:
            return {f"message": "Error inserting item {name}"}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item_from_db()
        return {"message": f"Item {name} deleted"}, 201

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()
        try:
            item = ItemModel.find_by_name(name)
            if item:
                item.price = request_data['price']
                item.store_id = request_data['store_id']
            else:
                item = ItemModel(name, **request_data)
            item.save_item_to_db()
            return item.json(), 201
        except:
            return {"message": f"Unable to update item {name}"}, 500


class Items(Resource):
    @jwt_required()
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}, 200
