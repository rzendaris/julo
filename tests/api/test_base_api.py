import json

from app.models.user_models import UserInfo
from tests.utils.base_test import BaseTest


class BaseApiTestCase(BaseTest):

    def set_up_extra(self):
        self.user_info = UserInfo(1, 'username', 'photo')
        self.user_info.save()

        self.default_headers = {
            'User-Id': self.user_info.id,
            'Username': 'username',
            'User-Photo': 'photo',
            'Content-Type': 'application/json'
        }

    def send_get(self, url, headers=None):
        if not headers:
            headers = self.default_headers
        return self.client.get(url, headers=headers)

    def send_post(self, url, data, headers=None):
        if not headers:
            headers = self.default_headers
        return self.client.post(url,
                                data=json.dumps(data),
                                headers=headers)

    def send_put(self, url, data, headers=None):
        if not headers:
            headers = self.default_headers
        return self.client.put(url,
                               data=json.dumps(data),
                               headers=headers)

    def send_delete(self, url, headers=None):
        if not headers:
            headers = self.default_headers
        return self.client.delete(url, headers=headers)
