from datetime import datetime
from typing import Any

from backend.models import Lot, Picture
from backend.types import AddLotPayload
from backend.services.db import db
from backend.exc import LotDoesNotExist, InvalidLotID, LotEndedError

from datetime import date


def create_picture(pictures: list[str], lot_id: int) -> None:

    # s3 backet for pictures logic here

    for img in pictures:
        #
        picture = Picture(
            url="received url",
            lot_id=lot_id,
        )
        db.session.add(picture)

    db.session.commit()
    return


def create_lot(payload: AddLotPayload, pictures: list, user_id: int) -> int:
    lot = Lot(
        lot_name=payload["lot_name"],
        description=payload["description"],
        author_id=user_id,
        creation_date=date.today(),
        end_date=payload["end_date"],
    )
    db.session.add(lot)
    db.session.commit()

    if pictures:
        create_picture(pictures, lot.id)

    return lot.id


def get_lot_by_id(lot_id: int) -> Lot | None:
    return Lot.query.filter(Lot.id == lot_id).one_or_none()


def validate_lot_id(raw_id: Any) -> int:
    try:
        lot_id = int(raw_id)
    except (TypeError, ValueError) as e:
        raise InvalidLotID from e

    lot = get_lot_by_id(lot_id)
    if lot is None:
        raise LotDoesNotExist

    return lot_id


def schema_lot_validator(value: int):
    lot = get_lot_by_id(value)
    if lot is None:
        raise LotDoesNotExist
    if lot.end_date <= datetime.now():
        raise LotEndedError
