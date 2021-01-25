from flask_restful import Resource, abort
from app import db, cache
from app.models import Mall, Unit, units_schema, unit_schema
from app.common.util import parser_unit, verify_relationship_consistency, try_add_item_to_db


class UnitsList(Resource):
    @cache.cached(timeout=50)
    def get(self, id=None, mall_id=None):
        if id and mall_id:
            verify_relationship_consistency(id, mall_id)
            units = Unit.query.filter_by(mall_id=mall_id)
        else:
            units = Unit.query.all()
        return units_schema.dump(units)

    def post(self, id=None, mall_id=None):
        """
        id and mall_id are not none where we use the long url
        """
        args = parser_unit.parse_args()
        self._verify_post_args(args, id, mall_id)
        new_unit = Unit(name=args['name'], mall_id=args['mall_id'])
        error = try_add_item_to_db(new_unit)
        if error:
            return "Item {} already exists".format(args['name']), 409
        return unit_schema.dump(new_unit), 201

    @staticmethod
    def _verify_post_args(args, id, mall_id):
        if not Mall.query.filter_by(id=args['mall_id']).first():
            abort(409, message="Mall id {} Doesn't exist".format(args['mall_id']))
        elif mall_id and mall_id != int(args['mall_id']):
            abort(409, message="Mall id {} is different from it's id given in the uri {}".
                  format(args['mall_id'], mall_id))
        else:
            verify_relationship_consistency(id, mall_id)


class Units(Resource):
    @cache.cached(timeout=50)
    def get(self, id, mall_id=None, unit_id=None):
        if mall_id and unit_id:
            verify_relationship_consistency(id, mall_id, unit_id)
            unit = Unit.query.get_or_404(unit_id)
        else:
            unit = Unit.query.get_or_404(id)
        return unit_schema.dump(unit)

    def delete(self, id, mall_id=None, unit_id=None):
        if mall_id and unit_id:
            verify_relationship_consistency(id, mall_id, unit_id)
            unit = Unit.query.get_or_404(unit_id)
        else:
            unit = Unit.query.get_or_404(id)
        db.session.delete(unit)
        db.session.commit()
        return '', 204

    def put(self, id, mall_id=None, unit_id=None):
        """
        HTTP PUT method allows a complete replacement of a document or to create it.
        todo: verify url consistency with args (account_id and unit_id can be in both args and url)
        """
        args = parser_unit.parse_args()
        unit, unit_id = self._find_unit_if_exists(args, id, mall_id, unit_id)

        if unit:
            # update
            unit.name = args['name']
            unit.mall_id = args['mall_id']
            code = 200
        else:
            # create
            unit = Unit(id=unit_id, name=args['name'], mall_id=args['mall_id'])
            code = 201

        error = try_add_item_to_db(unit)
        if error:
            return "Unit {} already exists".format(args['name']), 409
        return unit_schema.dump(unit), code

    def patch(self, id):
        """
        HTTP PATCH is used to modify an existing HTTP resource or to create if possible.
        (different for more than 1 attribute)
        on modifie le parser (parser_copy.remove_argument) où tout les éléments ne sont pas required jsute l'id et
        ceux qui sont donnés doivent être non nuls
        """
        return self.put(id)

    @staticmethod
    def _find_unit_if_exists(args, id, mall_id=None, unit_id=None):
        if not Mall.query.filter_by(id=args['mall_id']).first():
            abort(404, message="Item {} doesn't exist".format(id))
        elif unit_id:
            # shot url
            unit = Unit.query.filter_by(id=unit_id).first()
            return unit, unit_id
        else:
            # short url
            unit = Unit.query.filter_by(id=id).first()
            return unit, id
