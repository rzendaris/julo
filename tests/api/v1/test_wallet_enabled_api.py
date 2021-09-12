from app.constants.wallet_status_enum import WalletStatusEnum
from tests.api.test_base_api import BaseApiTestCase
from flask import url_for


class EnabledWalletApiTests(BaseApiTestCase):

    def test_invalid_authorization(self):
        token = "237562hjbahfejfhwehf"
        headers = {
            'Authorization': 'Token {0}'.format(token),
            'Content-Type': 'application/json'
        }
        request_data = {
            "customer_xid": self.user_info.customer_xid
        }
        result = self.send_post(url_for('wallet_v1.enable_wallet'), data=request_data, headers=headers)
        assert result.status_code == 401

    def test_enable_wallet_disabled_status(self):
        self.user_wallet.status = WalletStatusEnum.DISABLED.value
        self.user_wallet.save()

        request_data = {
            "customer_xid": self.user_info.customer_xid
        }
        result = self.send_post(url_for('wallet_v1.enable_wallet'), data=request_data)
        assert result.status_code == 201

    def test_enable_wallet_enabled_status(self):
        self.user_wallet.status = WalletStatusEnum.ENABLED.value
        self.user_wallet.save()

        request_data = {
            "customer_xid": self.user_info.customer_xid
        }
        result = self.send_post(url_for('wallet_v1.enable_wallet'), data=request_data)
        assert result.status_code == 400
