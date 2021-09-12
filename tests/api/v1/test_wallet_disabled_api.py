from app.constants.wallet_status_enum import WalletStatusEnum
from tests.api.test_base_api import BaseApiTestCase
from flask import url_for


class DisabledWalletApiTests(BaseApiTestCase):

    def test_invalid_authorization(self):
        token = "237562hjbahfejfhwehf"
        headers = {
            'Authorization': 'Token {0}'.format(token),
            'Content-Type': 'application/json'
        }
        request_data = {
            "is_disabled": True
        }
        result = self.send_patch(url_for('wallet_v1.disable_wallet'), data=request_data, headers=headers)
        assert result.status_code == 401

    def test_disable_wallet_disabled_status(self):
        self.user_wallet.status = WalletStatusEnum.DISABLED.value
        self.user_wallet.save()

        request_data = {
            "is_disabled": True
        }
        result = self.send_patch(url_for('wallet_v1.disable_wallet'), data=request_data)
        assert result.status_code == 400

    def test_disable_wallet_enabled_status(self):
        self.user_wallet.status = WalletStatusEnum.ENABLED.value
        self.user_wallet.save()

        request_data = {
            "is_disabled": True
        }
        result = self.send_patch(url_for('wallet_v1.disable_wallet'), data=request_data)
        assert result.status_code == 200
