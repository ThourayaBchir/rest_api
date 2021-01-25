from tests.base_case import BaseCase


class TestAccountsList(BaseCase):

    def test_get_accounts(self):
        response = self.client.get('/api/v1.0/accounts')

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json[0]['name'] == 'test_account_1'
        assert len(response.json[0]['malls']) == 2

    def test_post_account(self):
        data = {'name': 'test_account_3'}
        response = self.client.post('/api/v1.0/accounts', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_account_3'

    def test_post_duplicate_account(self):
        data = {'name': 'test_account_1'}
        response = self.client.post('/api/v1.0/accounts', json=data)

        assert response.status_code == 409
        assert response.json == 'Item {} already exists'.format(data['name'])

    def test_post_nullname_account(self):
        data = {'name': ''}
        response = self.client.post('/api/v1.0/accounts', json=data)

        assert response.status_code == 400


class TestAccounts(BaseCase):

    def test_get_account(self):
        response = self.client.get('/api/v1.0/accounts/1')

        assert response.status_code == 200
        assert response.json['id'] == 1

    def test_get_invalid_account(self):
        response = self.client.get('/api/v1.0/accounts/10')

        assert response.status_code == 404

    def test_delete_account(self):
        response = self.client.delete('/api/v1.0/accounts/2')

        assert response.status_code == 204

    def test_delete_invalid_account(self):
        response = self.client.delete('/api/v1.0/accounts/10')

        assert response.status_code == 404

    def test_put_new_account(self):
        data = {'name': 'test_account_4'}
        response = self.client.put('/api/v1.0/accounts/100', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_account_4'

    def test_put_existing_account(self):
        data = {'name': 'test_new_name'}
        response = self.client.put('/api/v1.0/accounts/1', json=data)

        assert response.status_code == 200
        assert response.json['name'] == 'test_new_name'
        assert response.json['id'] == 1
