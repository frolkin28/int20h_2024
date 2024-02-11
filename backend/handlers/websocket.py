from enum import Enum

from flask import current_app, request
from flask_socketio import Namespace
from marshmallow import ValidationError

from backend.lib.bets import (
    get_bets_for_display,
    serialize_bets,
    create_bet,
    serialize_new_bet,
)
from backend.exc import HigherBetExistsError, LotDoesNotExist, InvalidLotID
from backend.lib.auth import verify_user_token
from backend.lib.chat import (
    get_recent_messages,
    serialize_messages,
    create_message,
    serialize_new_message,
    validate_message,
)
from backend.lib.lots import validate_lot_id
from backend.lib.websocket import AuctionEvents, ChatEvents, BaseEvents
from backend.lib.schemas import BetCreationSchema


class BaseNamespace(Namespace):
    def on_connect(self):
        current_app.logger.info(
            f"Connected to {self.namespace} (socket_id: {request.sid})",
        )

    def on_disconnect(self):
        current_app.logger.info(
            f"Disconnected from {self.namespace} (socket_id: {request.sid})",
        )

    def emit_error_and_disconnect(self, event: Enum, message: str | dict):
        self.emit_message(event, message)
        self.disconnect(request.sid)

    def emit_message(self, event: Enum, message: str | dict):
        self.emit(event.value, {"message": message}, room=request.sid)


class BetsLogNamespace(BaseNamespace):
    def on_join_auction(self, data: dict):
        try:
            lot_id = validate_lot_id(data.get("lot_id"))
        except (LotDoesNotExist, InvalidLotID) as e:
            self.emit_error_and_disconnect(
                BaseEvents.JOIN_ERROR,
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
            self.emit_message(BaseEvents.UNAUTHORIZED, "Invalid JWT")
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
                BaseEvents.VALIDATION_ERROR,
                e.messages_dict,
            )
            return

        try:
            bet = create_bet(
                user_id=user.id,
                lot_id=bet_data["lot_id"],
                amount=bet_data["amount"],
            )
        except HigherBetExistsError as err:
            self.emit_message(
                BaseEvents.VALIDATION_ERROR,
                err.message,
            )
            return
        except Exception as e:
            current_app.logger.exception(e)
            return

        self.emit_message(AuctionEvents.BET_CREATION_SUCCESS, "Bet accepted")
        self.emit(
            AuctionEvents.BETS_LOG_UPDATE.value,
            serialize_new_bet(user, bet),
            room=data["lot_id"],
        )


class ChatNamespace(BaseNamespace):
    def on_join_chat(self, data: dict):
        try:
            lot_id = validate_lot_id(data.get("lot_id"))
        except (LotDoesNotExist, InvalidLotID) as e:
            self.emit_error_and_disconnect(
                BaseEvents.JOIN_ERROR,
                e.message,
            )
            return

        self.enter_room(sid=request.sid, room=lot_id)
        messages = serialize_messages(get_recent_messages(lot_id))
        self.emit(
            ChatEvents.CHAT_UPDATE.value,
            messages,
            room=request.sid,
        )

    def on_new_message(self, data: dict):
        user = verify_user_token(data.get("access_token"))
        if not user:
            self.emit_message(BaseEvents.UNAUTHORIZED, "Invalid JWT")
            return
        try:
            lot_id = validate_lot_id(data.get("lot_id"))
        except (LotDoesNotExist, InvalidLotID) as e:
            self.emit_message(
                BaseEvents.VALIDATION_ERROR,
                e.message,
            )
            return
        message = validate_message(data.get("message"))
        if not message:
            self.emit_message(
                BaseEvents.VALIDATION_ERROR,
                {"message": "Empty message is invalid"},
            )
            return

        created_message = create_message(
            user_id=user.id,
            lot_id=lot_id,
            message=message,
        )
        self.emit(
            ChatEvents.CHAT_UPDATE.value,
            serialize_new_message(user, created_message),
            room=lot_id,
        )
