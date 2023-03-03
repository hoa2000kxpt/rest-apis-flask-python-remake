import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from models.item import ItemModel
from schemas import ItemSchema, ItemUpdateSchema, StoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store


@blp.arguments(ItemUpdateSchema)
@blp.response(200, ItemSchema)
def put(self, item_data, item_id):
    item = ItemModel.query.get(item_id)
    if item:
        item.price = item_data["price"]
        item.name = item_data["name"]
    else:
        item = ItemModel(id=item_id, **item_data)

    db.session.add(item)
    db.session.commit()

    return item
