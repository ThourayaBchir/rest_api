from flask_restful import reqparse, abort
from app.models import Account, Mall
from app import db


def not_empty(value, name):
    if value in ['', "''"] or value is None:
        raise ValueError("The parameter '{}' is not valid. You sent the value: {}".format(name, value))
    return value


parser = reqparse.RequestParser(trim=True)
parser.add_argument('id', type=int)
parser.add_argument('name', required=True, type=not_empty)

parser_mall = parser.copy()
parser_mall.add_argument('account_id', required=True, type=not_empty)

parser_unit = parser.copy()
parser_unit.add_argument('mall_id', required=True, type=not_empty)


def verify_relationship_consistency(account_id, mall_id=None, unit_id=None):
    if account_id:
        account = Account.query.get_or_404(account_id)

    if mall_id and mall_id not in [mall_dict.id for mall_dict in account.malls]:
        return abort(404, message="Mall {} isn't in account {}".format(mall_id, account_id))

    if unit_id and unit_id not in [unit_dict.id for unit_dict in Mall.query.get_or_404(mall_id).units]:
        return abort(404, message="Unit {} isn't in Mall {}".format(unit_id, mall_id))


def try_add_item_to_db(item):
    try:
        db.session().add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
