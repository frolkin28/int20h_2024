from datetime import datetime
from typing import Any
from sqlalchemy.orm import joinedload
from flask import current_app
from sqlalchemy import desc


from werkzeug.datastructures import FileStorage


import boto3
from botocore.exceptions import ClientError

from backend.models import Lot, Picture, User, Bet
from backend.types import LotPayload, FullLotPayload, ListLotPayload, t
from backend.services.db import db
from backend.exc import (
    LotDoesNotExist,
    InvalidLotID,
    LotEndedError,
    InvalidDateError,
    UserDoesNotExist 
)

from datetime import date

from backend.exc import UserPermissionError


def upload_photo_to_s3(file: FileStorage, bucket_name: str, object_name: str) -> str:


    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_fileobj(file, bucket_name, object_name)
    except ClientError as e:
        current_app.logger.exception(e)

    return f"https://dq5d23gxa9vto.cloudfront.net/{object_name}"


def create_picture(pictures: list[FileStorage], lot_id: int) -> None:
    bucket_name = 'cha-cha-images' 

    object_prefix = str(lot_id)

    for img in pictures:
        object_name = f"{object_prefix}/{img.filename}"
        picture_url = upload_photo_to_s3(img, bucket_name, object_name)
        if picture_url:
            picture = Picture(
                url=picture_url,
                lot_id=lot_id)
            db.session.add(picture)

    db.session.commit()


def create_lot(payload: LotPayload, pictures: list[FileStorage], user_id: int) -> int:

    start_price = payload["start_price"] * 100

    lot = Lot(
        lot_name=payload["lot_name"],
        description=payload["description"],
        author_id=user_id,
        creation_date=date.today(),
        end_date=payload["end_date"],
        start_price=start_price
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


def update_lot_data(payload: LotPayload, user_id: int, lot_id: int) -> int:
    if payload["end_date"].date() < date.today():
        raise InvalidDateError

    lot = Lot.query.get(lot_id)

    if not lot:
        raise LotDoesNotExist

    if lot.end_date <= datetime.now():
        raise LotEndedError

    if user_id != lot.author_id:
        raise UserPermissionError

    lot.lot_name = payload["lot_name"]
    lot.description = payload["description"]
    lot.end_date = payload["end_date"]

    db.session.commit()

    return lot.id


def get_lot_data(id: int) -> dict:

    lot = Lot.query.get(id)
    author = User.query.get(lot.author_id)
    lot_pictures = Picture.query.filter(Picture.lot_id == id).all()
    
    if lot_pictures:
        picture_urls = [picture.url for picture in lot_pictures]
    else:
        picture_urls = []

    start_price = lot.start_price/100 if lot.start_price else None

    if lot:
        lot_payload: FullLotPayload = {
                "lot_name": lot.lot_name,
                "description": lot.description,
                "start_price": start_price,
                "author": {
                    "email": author.email,
                    "first_name": author.first_name,
                    "last_name": author.last_name
                },
                "creation_date": lot.creation_date,
                "end_date": lot.end_date,
                "pictures": picture_urls
            }

        return lot_payload
    else:
        return None


def main_page_data(page: int, per_page: int) -> list:
    data = []

    lots = Lot.query.paginate(page=page, per_page=per_page, error_out=False)
    for lot in lots.items:
        picture = Picture.query.filter(Picture.lot_id == lot.id).first()
        biggest_bet = Bet.query.filter(Bet.lot_id == lot.id).order_by(desc(Bet.amount)).first()
        price = float(biggest_bet.amount) if biggest_bet else float(lot.start_price)
        
        picture_url = picture.url if picture else None
        price_lot = price / 100 if price else None

        load_data: ListLotPayload = {
            "lot_name": lot.lot_name,
            "lot_id": lot.id,
            "end_date": lot.end_date,
            "picture": picture_url,
            "price": price_lot
        }
        data.append(load_data)
    return data
