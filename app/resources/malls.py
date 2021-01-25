from flask_restful import Resource, abort
from app import db, cache
from app.models import Account, Mall, malls_schema, mall_schema
from app.common.util import parser_mall, verify_relationship_consistency, try_add_item_to_db


class MallsList(Resource):
    @cache.cached(timeout=50)
    def get(self, id=None):
        if id:
            verify_relationship_consistency(id)
            malls = Mall.query.filter_by(account_id=id)
        else:
            malls = Mall.query.all()
        return malls_schema.dump(malls)

    def post(self, id=None):
        args = parser_mall.parse_args()
        self._verify_post_args(args, id)
        new_mall = Mall(name=args['name'], account_id=args['account_id'])
        error = try_add_item_to_db(new_mall)
        if error:
            return "Item {} already exists".format(args['name']), 409
        return mall_schema.dump(new_mall), 201

    @staticmethod
    def _verify_post_args(args, id):
        if not Account.query.filter_by(id=args['account_id']).first():
            abort(409, message="Account id {} Doesn't exist".format(args['account_id']))
        elif id and id != int(args['account_id']):
            abort(409, message="Account id {} is different from the uri {}".format(args['account_id'], id))


class Malls(Resource):
    @cache.cached(timeout=50)
    def get(self, **kwargs):
        if 'mall_id' in kwargs:
            verify_relationship_consistency(kwargs['id'], kwargs['mall_id'])
            response = Mall.query.get_or_404(kwargs['mall_id'])
        else:
            response = Mall.query.get_or_404(kwargs['id'])
        response = mall_schema.dump(response)
        return response

    def delete(self, **kwargs):
        if 'mall_id' in kwargs:
            verify_relationship_consistency(kwargs['id'], kwargs['mall_id'])
            response = Mall.query.get_or_404(kwargs['mall_id'])
        else:
            response = Mall.query.get_or_404(kwargs['id'])
        db.session.delete(response)
        db.session.commit()
        return '', 204

    def put(self, id, mall_id=None):
        """
        HTTP PUT method allows a complete replacement of a document or its creation.
        It changes the name or the associated account of an existing mall, or it creates a new mall,
        if the id of the mall in the url doesn't exit.
        todo: verify url consistency with args (account_id and mall_id can be in both args and url)
        """
        args = parser_mall.parse_args()
        mall, mall_id = self._find_mall_if_exists(args, id, mall_id)

        if mall:
            mall.name = args['name']
            mall.account_id = args['account_id']
            code = 200
        else:
            mall = Mall(id=mall_id, name=args['name'], account_id=args['account_id'])
            code = 201

        error = try_add_item_to_db(mall)
        if error:
            return "Item {} already exists".format(args['name']), 409
        return mall_schema.dump(mall), code

    def patch(self, **kwargs):
        """
        HTTP PATCH is used here as an alias for PUT
        """
        return self.put(**kwargs)

    @staticmethod
    def _find_mall_if_exists(args, id, mall_id=None):
        if not Account.query.filter_by(id=args['account_id']).first():
            abort(404, message="Account {} doesn't exist".format(args['account_id']))

        elif mall_id:
            # if long url
            mall = Mall.query.filter_by(id=mall_id).first()
            return mall, mall_id
        else:
            # if short url
            mall = Mall.query.filter_by(id=id).first()
            return mall, id
