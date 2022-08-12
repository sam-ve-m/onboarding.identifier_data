# Standards
from enum import IntEnum

# from Third party
from strenum import StrEnum


class QueueTypes(IntEnum):
    USER_IDENTIFIER_DATA = 4


class UserOnboardingStep(StrEnum):
    IDENTIFIER_DATA = "identifier_data"
