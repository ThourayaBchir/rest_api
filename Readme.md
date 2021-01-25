## Description

REST api to access the resources:
- Accounts 
- Malls
- Units

Where each mall is linked to a an account and each unit iis linked to an account.

### To set up and launch the app

```shell
git clone ...
cd ...

python3 -m venv api_venv 
source api_venv/bin/activate
pip install -r requirements.txt

flask init-db
python populate_db.py
```
### To run the app
```
python rest_api.py
```
or
```
flask run
```

### To run tests
```
tox
```

### Some examples to query

```
curl "http://localhost:5000/api/v1.0/accounts/1/malls/1/units"  -d "name=unit_name&mall_id=1" -X POST -v

curl "http://localhost:5000/api/v1.0/accounts"   -X GET -v

curl "http://localhost:5000/api/v1.0/accounts/1"   -X GET -v

curl "http://localhost:5000/api/v1.0/accounts/1" -d "name=account_update_name"  -X PUT -v

curl "http://localhost:5000/api/v1.0/accounts/1/malls/1" -d "name=mall_update_name&account_id=1"  -X PUT -v

curl "http://localhost:5000/api/v1.0/malls/1" -d "name=mall_update_name2&account_id=1"  -X PUT -v

```

