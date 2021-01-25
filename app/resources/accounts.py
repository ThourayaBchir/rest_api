from flask_restful import Resource, request
from app import db, cache
from app.models import Account, accounts_schema, account_schema
from app.common.util import parser, try_add_item_to_db
from flask import url_for


class AccountsList(Resource):
    @cache.cached(timeout=10)
    def get(self):
        if {'limit', 'page'}.issubset(set(request.args)):
            return self.pagination_response(request.args)

        accounts = Account.query.all()
        return accounts_schema.dump(accounts)

    def post(self):
        args = parser.parse_args()
        new_account = Account(name=args['name'])
        error = try_add_item_to_db(new_account)
        if error:
            return "Item {} already exists".format(args['name']), 409
        return account_schema.dump(new_account), 201

    def pagination_response(self, page_args):
        if page_args.get('limit', None).isdigit() and \
                page_args.get('page', None).isdigit():

            limit = int(page_args.get('limit', None))
            page = int(page_args.get('page', None))
            accounts = Account.query.paginate(page=page, per_page=limit)
            next_page = accounts.next_num
            url = url_for('accountslist', page=next_page, limit=limit)
            total = accounts.total
            return accounts_schema.dump(accounts.items) + \
                [{'metadata': {'page': page, 'per_page': limit, 'total_count': total, 'next_page': url}}]


class Accounts(Resource):
    @cache.cached(timeout=50)
    def get(self, id):
        account = Account.query.get_or_404(id)
        account = account_schema.dump(account)
        return account

    def delete(self, id):
        account = Account.query.get_or_404(id)
        db.session.delete(account)
        db.session.commit()
        return '', 204

    def put(self, id):
        """
        HTTP PUT method allows a complete replacement of a document or its creation.
        """
        args = parser.parse_args()
        account = Account.query.get(id)
        if account:
            account.name = args['name']
            code = 200
        else:
            account = Account(id=id, name=args['name'])
            code = 201
        try_add_item_to_db(account)
        return account_schema.dump(account), code

    def patch(self, id):
        """
        Alias for the put method
        """
        return self.put(id)
