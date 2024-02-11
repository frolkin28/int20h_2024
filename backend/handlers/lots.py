from typing import cast
from backend.utils import error_response, success_response

from flask import Blueprint, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user

from backend.lib.schemas import LotSchema, LotCreationSchema, FullLotSchema, ListLotSchema
from backend.types import LotCreationLoad, LotPayload

from backend.lib.lots import create_lot, update_lot_data, get_lot_data, main_page_data
from backend.exc import (
    InvalidDateError,
    LotDoesNotExist,
    LotEndedError,
    UserPermissionError,
)


bp = Blueprint("lots", __name__, url_prefix="/api/lots")


@bp.route("/", methods=("POST",))
@jwt_required()
def add_lot():
    """
    ---
    post:
        summary: Створити лот
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
                            start_price:
                                type: float 
                            images:
                                type: array
                                items:
                                    type: string
                                    format: binary
        responses:
            '200':
                content:
                    application/json:
                        schema: UpsertLotSuccessResponse
            '400':
                content:
                    application/json:
                        schema: UpsertLotSuccessResponse
            '401':
                description: Користувач не авторизований
        tags:
        - lots
    """
    user_id: int = current_user.id

    try:
        request_data = cast(
            LotCreationLoad,
            LotCreationSchema().load(
                {
                    "lot_name": request.form.get("lot_name"),
                    "description": request.form.get("description"),
                    "end_date": request.form.get("end_date"),
                    "start_price": request.form.get("start_price"),
                }
            ),
        )
    except ValidationError as e:
        return error_response(status_code=400, errors=e.messages)

    request_pictures = request.files.getlist("images")
    lot_id = create_lot(request_data, request_pictures, user_id)

    return success_response(data={"lot_id": lot_id})


@bp.route("/<int:id>", methods=("PUT",))
@jwt_required()
def update_lot(id):
    """
    ---
    put:
        summary: Редагування лоту
        requestBody:
            content:
                application/json:
                    schema: LotSchema
        responses:
            '200':
                content:
                    application/json:
                        schema: UpsertLotSuccessResponse
            '400':
                content:
                    application/json:
                        schema: 
                             oneOf:
                                - UpsertLotErrorResponse
                                - ErrorMessageResponse
            '401':
                description: Користувач не авторизований
            '403':
                content:
                    application/json:
                        schema: ErrorMessageResponse
        tags:
        - lots
    """
    user_id = current_user.id

    try:
        request_data = cast(
            LotPayload,
            LotSchema().load(
                {
                    "lot_name": request.form.get("lot_name"),
                    "description": request.form.get("description"),
                    "end_date": request.form.get("end_date"),
                }
            ),
        )
    except ValidationError as e:
        return error_response(status_code=400, errors=e.messages)

    try:
        lot_id = update_lot_data(request_data, user_id, id)
    except (InvalidDateError, LotDoesNotExist, LotEndedError) as e:
        return error_response(
            status_code=400,
            errors={"message": e.message},
        )
    except UserPermissionError as e:
        return error_response(
            status_code=403,
            errors={"message": e.message},
        )

    return success_response(data={"lot_id": lot_id})


@bp.route("/<int:id>", methods=("GET",))
def lot_data(id):
    """
    ---
    get:
        summary: Сторінка лоту
        responses:
            '200':
                content:
                    application/json:
                        schema: FullLotSchema
            '400':
                content:
                    application/json:
                        schema: 
                             oneOf:
                                - UpsertLotErrorResponse
                                - ErrorMessageResponse
            '403':
                content:
                    application/json:
                        schema: ErrorMessageResponse
        tags:
        - lots
    """

    try:
        lot_data = get_lot_data(id)
    except (InvalidDateError, LotDoesNotExist) as e:
        return error_response(
            status_code=400,
            errors={"message": e.message},
        )


    return success_response(data={"lot_data": lot_data})


@bp.route("/", methods=("GET",))
def main_page():
    """
    ---
    get:
        summary: Список лотів
        responses:
            '200':
                content:
                    application/json:
                        schema: ListLotSchema
            '400':
                content:
                    application/json:
                        schema: 
                             oneOf:
                                - UpsertLotErrorResponse
                                - ErrorMessageResponse
        tags:
        - lots
    """

    try:
        page = request.args.get('page', 1, type=int)
        per_page = 13
        lot_list = main_page_data(page, per_page)
        has_more_items = True if len(lot_list) == per_page else False
    except (InvalidDateError, ValidationError) as e:
        return error_response(
            status_code=400,
            errors={"message": e.message},
        )
    return success_response(data={"lot_data": lot_list[:per_page-1], "has_more_items": has_more_items})
