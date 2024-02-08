from typing import cast

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from backend.lib.auth import with_auth_user

from backend.lib.schemas import AddLotSchema
from backend.types import AddLotPayload
from backend.models import User

from backend.lib.lots import create_lot


bp = Blueprint("lots", __name__, url_prefix="/api/lots")


@bp.route("/add_lot", methods=("POST",))
@with_auth_user
def add_lot(user: User):
    """
    ---
    post:
        summary: add lot
        requestBody:
            content:
              application/json:
                schema:
                  AddLotSchema
        responses:
            '200':
                content:
                    application/json:
                        schema: LotResponse
            '400':
                content:
                    application/json:
                        schema: ValidationError
        tags:
        - lots
    """
    user_id = user.id

    try:
        request_data = cast(
            AddLotPayload,
            AddLotSchema().load(
                {
                    "lot_name": request.form.get("lot_name"),
                    "description": request.form.get("description"),
                    "end_date": request.form.get("end_date"),
                }
            ),
        )
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    request_pictures = request.files.getlist("file")
    lot_id = create_lot(request_data, request_pictures, user_id)

    response = jsonify({"lot_id": lot_id})
    return response
