from datetime import datetime
from decimal import Decimal

from backend.exc import HigherBetExistsError
from backend.models import Bet, User, Lot
from backend.services.db import transaction, db
from backend.types import BetForDisplay, UserForDisplay


def prepare_amount(amount: int) -> str:
    formatted_string = "{:.2f}".format(float(amount) / 100)
    return formatted_string


def get_bets_for_display(lot_id: int) -> list[BetForDisplay]:
    # TODO: (frolkin28) add pagination here, after testing

    query = (
        Bet.query.join(User, Bet.user_id == User.id)
        .with_entities(
            Bet.id,
            Bet.amount,
            Bet.creation_date,
            User.id.label("user_id"),
            User.email.label("user_email"),
            User.first_name.label("user_first_name"),
            User.last_name.label("user_last_name"),
        )
        .filter(Bet.lot_id == lot_id)
    )
    return [
        BetForDisplay(
            id=bet.id,
            lot_id=lot_id,
            amount=prepare_amount(bet.amount),
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


def create_bet(user_id: int, lot_id: int, amount: Decimal) -> Bet:
    with transaction():
        lot = Lot.query.get(lot_id)

        prepared_amount = int(amount * 100)  # в копійки
        if (prepared_amount <= lot.start_price):
            raise HigherBetExistsError

        last_bet = (
            Bet.query.filter(Bet.lot_id == lot_id).order_by(Bet.id.desc()).first()
        )
        if last_bet and prepared_amount <= last_bet.amount:
            raise HigherBetExistsError

        bet = Bet(
            user_id=user_id,
            lot_id=lot_id,
            amount=prepared_amount,
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
            amount=prepare_amount(bet.amount),
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
