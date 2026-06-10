"""MagicSquare_xx — 4×4 부분 마방진 검증."""

from magicxx.rules import MAGIC_SUM
from magicxx.verify import ConditionResult, ConditionStatus, VerifyResult, verify_grid

__all__ = [
    "MAGIC_SUM",
    "ConditionResult",
    "ConditionStatus",
    "VerifyResult",
    "verify_grid",
]
