from app import db, ma


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    malls = db.relationship('Mall', backref='accountid', cascade="all, delete")


class Mall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id', onupdate="CASCADE", ondelete="CASCADE"), index=True)
    units = db.relationship('Unit', cascade="all, delete")


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    mall_id = db.Column(db.Integer, db.ForeignKey('mall.id', onupdate="CASCADE", ondelete="CASCADE"), index=True)


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        load_instance = True
    id = ma.auto_field()
    name = ma.auto_field()
    malls = ma.List(ma.HyperlinkRelated("malls", external=True))
    self = ma.Hyperlinks(ma.AbsoluteURLFor('accounts', values=dict(id='<id>')))


class MallSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mall
        load_instance = True
    id = ma.auto_field()
    name = ma.auto_field()
    account_id = ma.auto_field()
    units = ma.List(ma.HyperlinkRelated("units", external=True))
    self = ma.Hyperlinks(ma.AbsoluteURLFor('malls', values=dict(id='<id>')))


class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit
        load_instance = True
    id = ma.auto_field()
    name = ma.auto_field()
    mall_id = ma.auto_field()
    self = ma.Hyperlinks(ma.AbsoluteURLFor('units', values=dict(id='<id>')))


accounts_schema = AccountSchema(many=True)
account_schema = AccountSchema()

malls_schema = MallSchema(many=True)
mall_schema = MallSchema()

units_schema = UnitSchema(many=True)
unit_schema = UnitSchema()
