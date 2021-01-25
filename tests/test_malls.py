from tests.base_case import BaseCase


class TestMallsList(BaseCase):

    def test_get_malls(self):
        response = self.client.get('/api/v1.0/malls')

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json[0]['name'] == 'test_mall_1'
        assert len(response.json[0]['units']) == 1

    def test_post_mall(self):
        data = {'name': 'test_mall_3', 'account_id': 1}
        response = self.client.post('/api/v1.0/malls', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_mall_3'
        assert response.json['account_id'] == 1
        assert self._is_url(response.json['self'])

    def test_post_duplicate_mall(self):
        data = {'name': 'test_mall_1', 'account_id': 1}
        response = self.client.post('/api/v1.0/malls', json=data)

        assert response.status_code == 409
        assert response.json == 'Item {} already exists'.format(data['name'])

    def test_post_incomplete_data_mall(self):
        data = {'name': 'test_mall_1'}
        response = self.client.post('/api/v1.0/malls', json=data)

        assert response.status_code == 400

    def test_post_mall_with_nonexistent_account(self):
        data = {'name': 'test_mall_1', 'account_id': 10}
        response = self.client.post('/api/v1.0/malls', json=data)

        assert response.status_code == 409

    def test_post_mall_with_empty_name(self):
        data = {'name': "", 'account_id': 1}
        response = self.client.post('/api/v1.0/malls', json=data)

        assert response.status_code == 400

    def test_post_mall_long_url(self):
        data = {'name': 'test_mall_10', 'account_id': 1}
        response = self.client.post('/api/v1.0/accounts/1/malls', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_mall_10'
        assert response.json['account_id'] == 1


class TestMalls(BaseCase):

    def test_get_mall(self):
        response = self.client.get('/api/v1.0/malls/1')

        assert response.status_code == 200
        assert response.json['id'] == 1

    def test_get_invalid_mall(self):
        response = self.client.get('/api/v1.0/malls/10')

        assert response.status_code == 404

    def test_delete_mall(self):
        response = self.client.delete('/api/v1.0/malls/2')

        assert response.status_code == 204

    def test_delete_invalid_mall(self):
        response = self.client.delete('/api/v1.0/malls/10')

        assert response.status_code == 404

    def test_put_new_mall(self):
        data = {'name': 'test_mall_4', 'account_id': 1}
        response = self.client.put('/api/v1.0/malls/100', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_mall_4'
        assert response.json['id'] == 100
        assert response.json['account_id'] == 1

    def test_put_existing_mall(self):
        data = {'name': 'test_new_name', 'account_id': 2}
        response = self.client.put('/api/v1.0/malls/1', json=data)

        assert response.status_code == 200
        assert response.json['name'] == 'test_new_name'
        assert response.json['id'] == 1
        assert response.json['account_id'] == 2

    def test_put_new_mall_long_url(self):
        data = {'name': 'test_mall_5', 'account_id': 1}
        response = self.client.put('/api/v1.0/accounts/1/malls/1000', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_mall_5'
        assert response.json['id'] == 1000
        assert response.json['account_id'] == 1

    def test_put_existing_mall_long_url(self):
        data = {'name': 'test_update_name_1', 'account_id': 1}
        response = self.client.put('/api/v1.0/accounts/1/malls/2', json=data)

        assert response.status_code == 200
        assert response.json['name'] == 'test_update_name_1'
        assert response.json['id'] == 2
        assert response.json['account_id'] == 1

    def test_put_mall_with_invalid_account(self):
        data = {'name': 'test_mall_update', 'account_id': 100}
        response = self.client.put('/api/v1.0/malls/2', json=data)

        assert response.status_code == 404

