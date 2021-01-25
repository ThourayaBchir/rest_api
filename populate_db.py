import os
from app.models import Account, Mall, Unit
from app import db, app

db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
if db_uri:
    os.remove('/'+db_uri.strip('sqlite:///'))

db.create_all()

for i in range(1, 30):
    db.session().add(Account(name='account_'+str(i)))
    db.session().add(Mall(name='mall_'+str(i), account_id=i))
    db.session().add(Unit(name='unit_'+str(i), mall_id=i))

db.session().commit()

print('Done')
