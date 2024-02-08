from enum import Enum


class AuctionEvents(Enum):
    AUCTION_JOIN_ERROR = "auction_join_error"
    BETS_LOG_UPDATE = "bets_log_update"
    UNAUTHORIZED = "unauthorized"
    BET_CREATION_SUCCESS = "bet_creation_success"
