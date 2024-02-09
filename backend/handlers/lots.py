from typing import cast
from backend.utils import error_response, success_response

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user

from backend.lib.schemas import AddLotSchema
from backend.types import AddLotPayload

from backend.lib.lots import create_lot


bp = Blueprint("lots", __name__, url_prefix="/api/lots")


@bp.route("/add_lot", methods=("POST",))
@jwt_required()
def add_lot():
    """
    ---
    post:
        summary: add lot
        requestBody:
            required: true
            content:
                multipart/form-data:
                    schema:
                        type: object
                        properties:
                            lot_name:
                                type: string
                            description:
                                type: string
                            end_date:
                                type: string
                                description: (iso, rfc, timestamp format)
                            files:
                                type: array
                                items:
                                    type: string
                                    format: binary
        responses:
            '200':
                content:
                    application/json:
                        schema: CreateLotSuccessResponse
            '400':
                content:
                    application/json:
                        schema: CreateLotErrorResponse
            '401':
                description: Користувач не авторизований
        tags:
        - lots
    """
    user_id: int = current_user.id

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
        return error_response(status_code=400, errors=e.messages)

    request_pictures = request.files.getlist("images")
    lot_id = create_lot(request_data, request_pictures, user_id)

    return success_response(data={"lot_id": lot_id})
