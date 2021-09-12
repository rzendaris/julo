from app.constants.wallet_status_enum import WalletStatusEnum
from tests.api.test_base_api import BaseApiTestCase
from flask import url_for


class BalanceWalletApiTests(BaseApiTestCase):

    def test_invalid_authorization(self):
        token = "237562hjbahfejfhwehf"
        headers = {
            'Authorization': 'Token {0}'.format(token),
            'Content-Type': 'application/json'
        }
        result = self.send_get(url_for('wallet_v1.get_wallet'), headers=headers)
        assert result.status_code == 401

    def test_get_wallet_disabled_status(self):
        result = self.send_get(url_for('wallet_v1.get_wallet'))
        assert result.status_code == 404

    def test_get_wallet_enabled_status(self):
        self.user_wallet.status = WalletStatusEnum.ENABLED.value
        self.user_wallet.save()

        result = self.send_get(url_for('wallet_v1.get_wallet'))
        assert result.status_code == 200
