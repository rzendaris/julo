import json
import jwt

from flask import current_app
from datetime import datetime, timedelta

from app.constants.wallet_status_enum import WalletStatusEnum
from app.models.user_models import UserInfo
from app.models.wallet_models import Wallet
from tests.utils.base_test import BaseTest


class BaseApiTestCase(BaseTest):

    def set_up_extra(self):
        self.user_info = UserInfo('ea0212d3-abd6-406f-8c67-868e814a2436')
        self.user_info.save()

        self.user_wallet = Wallet(self.user_info.customer_xid, WalletStatusEnum.DISABLED.value, 0)
        self.user_wallet.save()

        token = jwt.encode({
            'customer_xid': self.user_info.customer_xid,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config.get('JWT_SECRET_KEY'))

        self.default_headers = {
            'Authorization': 'Token {0}'.format(token.decode('utf-8')),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def send_get(self, url, headers=None):
        if not headers:
            headers = self.default_headers
        return self.client.get(url, headers=headers)

    def send_post(self, url, data, headers=None):
        if not headers:
            headers = self.default_headers
        return self.client.post(url,
                                data=data,
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

    def send_patch(self, url, data, headers=None):
        if not headers:
            headers = self.default_headers
        return self.client.patch(url,
                                 data=data,
                                 headers=headers)
