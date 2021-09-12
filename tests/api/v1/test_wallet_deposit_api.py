from app.constants.wallet_status_enum import WalletStatusEnum, DepositStatusEnum
from app.models.deposit_models import Deposit
from tests.api.test_base_api import BaseApiTestCase
from flask import url_for


class DepositWalletApiTests(BaseApiTestCase):

    def test_invalid_authorization(self):
        token = "237562hjbahfejfhwehf"
        headers = {
            'Authorization': 'Token {0}'.format(token),
            'Content-Type': 'application/json'
        }
        request_data = {
            "amount": 100000,
            "reference_id": "12345"
        }
        result = self.send_post(url_for('wallet_v1.deposit_wallet'), data=request_data, headers=headers)
        assert result.status_code == 401

    def test_deposit_wallet_disabled_status(self):
        self.user_wallet.status = WalletStatusEnum.DISABLED.value
        self.user_wallet.save()

        request_data = {
            "amount": 100000,
            "reference_id": "12345"
        }
        result = self.send_post(url_for('wallet_v1.deposit_wallet'), data=request_data)
        assert result.status_code == 404

    def test_deposit_wallet_invalid_request(self):
        self.user_wallet.status = WalletStatusEnum.ENABLED.value
        self.user_wallet.save()

        request_data_1 = {
            "amount": 100000,
        }
        result_1 = self.send_post(url_for('wallet_v1.deposit_wallet'), data=request_data_1)
        assert result_1.status_code == 400

        request_data_2 = {
            "reference_id": "12345"
        }
        result_2 = self.send_post(url_for('wallet_v1.deposit_wallet'), data=request_data_2)
        assert result_2.status_code == 400

        request_data_3 = {
            "amount": 0,
            "reference_id": "12345"
        }
        result_3 = self.send_post(url_for('wallet_v1.deposit_wallet'), data=request_data_3)
        assert result_3.status_code == 400

    def test_deposit_wallet_duplicate_reference_id(self):
        self.user_wallet.status = WalletStatusEnum.ENABLED.value
        self.user_wallet.save()

        deposit = Deposit(self.user_info.customer_xid, DepositStatusEnum.SUCCESS.value, 100000, "12345")
        deposit.save()

        request_data = {
            "amount": 100000,
            "reference_id": "12345"
        }
        result = self.send_post(url_for('wallet_v1.deposit_wallet'), data=request_data)
        assert result.status_code == 400

    def test_deposit_wallet_enabled_status(self):
        self.user_wallet.status = WalletStatusEnum.ENABLED.value
        self.user_wallet.save()

        request_data = {
            "amount": 100000,
            "reference_id": "12345"
        }
        result = self.send_post(url_for('wallet_v1.deposit_wallet'), data=request_data)
        assert result.status_code == 201
