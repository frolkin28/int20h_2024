from logging import getLogger
from typing import cast

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from backend.lib.auth import login_required

from backend.lib.schemas import AddLotSchema
from backend.types import AddLotPayload
from backend.lib.lots import (
    create_lot
)

log = getLogger(__name__)

bp = Blueprint("lots", __name__, url_prefix="/api/lots")


@bp.route("/add_lot", methods=("POST",))
@login_required
def add_lot():
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

    user_id = get_jwt_identity

    try:
        request_data = cast(
            AddLotPayload,
            AddLotSchema().load({
                "lot_name": request.form['lot_name'],
                "description": request.form['description'],
                "end_date": request.form['end_date'],
            })
        )

        if 'file' not in request.files:
            request_pictures = None
        else:
            request_pictures = request.files.getlist('file')

        lot_id = create_lot(request_data, request_pictures, user_id)

    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    
    response = jsonify({"lot_id": lot_id})
    return response
