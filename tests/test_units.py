from tests.base_case import BaseCase


class TestUnitsList(BaseCase):

    def test_get_units(self):
        response = self.client.get('/api/v1.0/units')

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json[0]['name'] == 'test_unit_1'

    def test_post_unit(self):
        data = {'name': 'test_unit_3', 'mall_id': 1}
        response = self.client.post('/api/v1.0/units', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_unit_3'
        assert response.json['mall_id'] == 1
        assert self._is_url(response.json['self'])

    def test_post_duplicate_unit(self):
        data = {'name': 'test_unit_1', 'mall_id': 1}
        response = self.client.post('/api/v1.0/units', json=data)

        assert response.status_code == 409
        assert response.json == 'Item {} already exists'.format(data['name'])

    def test_post_incomplete_data_unit(self):
        data = {'name': 'test_unit_1'}
        response = self.client.post('/api/v1.0/units', json=data)

        assert response.status_code == 400

    def test_post_unit_with_nonexistent_mall(self):
        data = {'name': 'test_unit_10', 'mall_id': 10}
        response = self.client.post('/api/v1.0/units', json=data)

        assert response.status_code == 409

    def test_post_unit_with_empty_name(self):
        data = {'name': "", 'mall_id': 1}
        response = self.client.post('/api/v1.0/malls', json=data)

        assert response.status_code == 400


class TestUnits(BaseCase):

    def test_get_unit(self):
        response = self.client.get('/api/v1.0/units/1')

        assert response.status_code == 200
        assert response.json['id'] == 1

    def test_get_invalid_unit(self):
        response = self.client.get('/api/v1.0/units/10')

        assert response.status_code == 404

    def test_delete_unit(self):
        response = self.client.delete('/api/v1.0/units/2')

        assert response.status_code == 204

    def test_delete_invalid_unit(self):
        response = self.client.delete('/api/v1.0/units/10')

        assert response.status_code == 404

    def test_put_new_unit(self):
        data = {'name': 'test_unit_3', 'mall_id': 1}
        response = self.client.put('/api/v1.0/units/100', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_unit_3'
        assert response.json['id'] == 100
        assert response.json['mall_id'] == 1

    def test_put_existing_unit(self):
        data = {'name': 'test_update_name', 'mall_id': 2}
        response = self.client.put('/api/v1.0/units/1', json=data)

        assert response.status_code == 200
        assert response.json['name'] == 'test_update_name'
        assert response.json['id'] == 1
        assert response.json['mall_id'] == 2

    def test_put_new_unit_long_url(self):
        data = {'name': 'test_unit_5', 'mall_id': 1}
        response = self.client.put('/api/v1.0/accounts/1/malls/1/units/1000', json=data)

        assert response.status_code == 201
        assert response.json['name'] == 'test_unit_5'
        assert response.json['id'] == 1000
        assert response.json['mall_id'] == 1

    def test_put_existing_unit_long_url(self):
        data = {'name': 'test_update_name_1', 'mall_id': 2}
        response = self.client.put('/api/v1.0/accounts/1/malls/2/units/1', json=data)

        assert response.status_code == 200
        assert response.json['name'] == 'test_update_name_1'
        assert response.json['id'] == 1
        assert response.json['mall_id'] == 2

    def test_put_unit_with_invalid_mall(self):
        data = {'name': 'test_unit_update', 'mall_id': 100}
        response = self.client.put('/api/v1.0/unit/2', json=data)

        assert response.status_code == 404

