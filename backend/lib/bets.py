from datetime import datetime
from backend.models import Bet, User
from backend.services.db import db
from backend.lib.schemas import BetResponseSchema
from backend.types import BetForDisplay, UserForDisplay


def get_bets_for_display(lot_id: int) -> list[BetForDisplay]:
    # TODO: (frolkin28) add pagination here, after testing

    user_alias = db.aliased(User)
    query = (
        db.session.query(
            Bet.id,
            Bet.amount,
            Bet.creation_date,
            user_alias.id.label("user_id"),
            user_alias.email.label("user_email"),
            user_alias.first_name.label("user_first_name"),
            user_alias.last_name.label("user_last_name"),
        )
        .join(User, Bet.user_id == User.id)
        .filter(Bet.lot_id == lot_id)
    )
    return [
        BetForDisplay(
            id=bet.id,
            lot_id=lot_id,
            amount=bet.amount,
            creation_date=bet.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
            author=UserForDisplay(
                id=bet.user_id,
                email=bet.user_email,
                first_name=bet.user_first_name,
                last_name=bet.user_last_name,
            ),
        )
        for bet in query
    ]


def create_bet(user_id: int, lot_id: int, amount: int) -> Bet:
    bet = Bet(
        user_id=user_id,
        lot_id=lot_id,
        amount=amount,
        creation_date=datetime.now(),
    )
    db.session.add(bet)
    db.session.commit()

    return bet


def serialize_bets(bets: list[BetForDisplay]) -> dict:
    return {"bets": bets}


def serialize_new_bet(user: User, bet: Bet) -> dict:
    bets_for_display = [
        BetForDisplay(
            id=bet.id,
            lot_id=bet.lot_id,
            amount=bet.amount,
            creation_date=bet.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
            author=UserForDisplay(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            ),
        )
    ]
    return serialize_bets(bets_for_display)
