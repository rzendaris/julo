
from enum import Enum


class WalletStatusEnum(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class DepositStatusEnum(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class WithdrawalStatusEnum(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
