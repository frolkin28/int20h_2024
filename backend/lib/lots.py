from datetime import datetime
from typing import Any

import boto3
from botocore.exceptions import ClientError

from backend.models import Lot, Picture, User
from backend.types import LotPayload, FullLotPayload, t
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


def upload_photo_to_s3(file_path: str, bucket_name: str, object_name: str) -> str:

    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        print(e)
        return None

    return f"https://dq5d23gxa9vto.cloudfront.net/{object_name}"


def create_picture(pictures: list[str], lot_id: int) -> None:
    bucket_name = 'cha-cha-images' 

    object_prefix = str(lot_id)

    for img in pictures:
        object_name = f"{object_prefix}/{img}" 
        picture_url = upload_photo_to_s3(img, bucket_name, object_name)
        if picture_url:
            picture = Picture(
                url=picture_url,
                lot_id=lot_id)
            db.session.add(picture)

    db.session.commit()


def create_lot(payload: LotPayload, pictures: t.List[str], user_id: int) -> int:
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

    try:
        lot = Lot.query.get(id)
    except:
        raise LotDoesNotExist
    
    try:
        author = User.query.get(lot.id)
    except:
        UserDoesNotExist

    lot_pictures = Picture.query.filter(Picture.lot_id == id).all()
    
    if lot_pictures:
        picture_urls = [picture.url for picture in lot_pictures]
    else:
        picture_urls = []

    lot_payload: FullLotPayload = {
            "lot_name": lot.lot_name,
            "description": lot.description,
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




