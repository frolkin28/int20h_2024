from enum import Enum


class BaseEvents(Enum):
    JOIN_ERROR = "join_error"
    UNAUTHORIZED = "unauthorized"
    VALIDATION_ERROR = "validation_error"


class AuctionEvents(Enum):
    BETS_LOG_UPDATE = "bets_log_update"
    BET_CREATION_SUCCESS = "bet_creation_success"


class ChatEvents(Enum):
    CHAT_UPDATE = "chat_update"
