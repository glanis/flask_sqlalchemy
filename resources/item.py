from models.item import ItemModel

from flask_restful import Resource, reqparse

from flask_jwt import jwt_required




class Item(Resource):
    #TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item belongs to a store!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404



    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        item =ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json()



    @jwt_required()
    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {"message": "item {name} not found".format(name)}





    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        elif data['price']:
            item.price = data['price']
        elif data['store_id']:
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
