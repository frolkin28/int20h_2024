from backend.lib.auth import verify_user_token
from flask import current_app, request
from flask_socketio import Namespace
from marshmallow import ValidationError

from backend.lib.bets import (
    get_bets_for_display,
    serialize_bets,
    create_bet,
    serialize_new_bet,
)
from backend.lib.lots import validate_lot_id
from backend.lib.websocket import AuctionEvents
from backend.exc import LotDoesNotExist, InvalidLotID
from backend.lib.schemas import BetCreationSchema


class BetsLogNamespace(Namespace):
    def on_connect(self):
        current_app.logger.info(
            f"Connected to {self.namespace} (socket_id: {request.sid})",
        )

    def on_disconnect(self):
        current_app.logger.info(
            f"Disconnected from {self.namespace} (socket_id: {request.sid})",
        )

    def on_join_auction(self, data: dict):
        try:
            lot_id = validate_lot_id(data.get("lot_id"))
        except (LotDoesNotExist, InvalidLotID) as e:
            self.emit_error_and_disconnect(
                AuctionEvents.AUCTION_JOIN_ERROR,
                e.message,
            )
            return

        self.enter_room(sid=request.sid, room=lot_id)
        json_response = serialize_bets(get_bets_for_display(lot_id))
        self.emit(
            AuctionEvents.BETS_LOG_UPDATE.value,
            json_response,
            room=request.sid,
        )

    def on_bet(self, data: dict):
        user = verify_user_token(data.get("access_token"))
        if not user:
            self.emit_message(AuctionEvents.UNAUTHORIZED, "Invalid JWT")
            return

        try:
            bet_data = BetCreationSchema().load(
                {
                    "lot_id": data.get("lot_id"),
                    "amount": data.get("amount"),
                }
            )
        except ValidationError as e:
            self.emit_message(
                AuctionEvents.BET_CREATION_ERROR,
                e.messages_dict,
            )
            return

        bet = create_bet(
            user_id=user.id,
            lot_id=bet_data["lot_id"],
            amount=bet_data["amount"],
        )

        self.emit_message(AuctionEvents.BET_CREATION_SUCCESS, "Bet accepted")
        self.emit(
            AuctionEvents.BETS_LOG_UPDATE.value,
            serialize_new_bet(user, bet),
            room=data["lot_id"],
        )

    def emit_error_and_disconnect(self, event: AuctionEvents, message: str | dict):
        self.emit_message(event, message)
        self.disconnect(request.sid)

    def emit_message(self, event: AuctionEvents, message: str | dict):
        self.emit(event.value, {"message": message}, room=request.sid)
