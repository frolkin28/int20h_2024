
from backend.models import Lot, Picture
from backend.types import AddLotPayload, t
from backend.services.db import db

from datetime import date


def create_picture(pictures: t.List[str] , lot_id: int) -> None:

    # s3 backet for pictures logic here
    
    for img in pictures:
        # 
        picture = Picture(
            url= "received url",
            lot_id=lot_id,
        )
        db.session.add(picture)

    db.session.commit()
    return

def create_lot(payload: AddLotPayload, pictures, user_id: int) -> int:
    lot = Lot(
        lot_name=payload["lot_name"],
        description=payload["description"],
        author_id = user_id,
        creation_date=date.today(),
        end_date=payload["end_date"]
    )
    db.session.add(lot)
    db.session.commit()

    if pictures:
        create_picture(pictures, lot.id)

    return lot.id
