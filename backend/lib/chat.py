from datetime import datetime

from backend.models import Message, User
from backend.services.db import db
from backend.types import MessageForDisplay, UserForDisplay


RECENT_MESSAGES_AMOUNT = 20


def create_message(user_id: int, lot_id: int, message: str) -> Message:
    message = Message(
        content=message,
        user_id=user_id,
        lot_id=lot_id,
        created_at=datetime.now(),
    )
    db.session.add(message)
    db.session.commit()

    return message


def get_recent_messages(lot_id: int) -> list[MessageForDisplay]:
    query = (
        Message.query.join(User, Message.user_id == User.id)
        .with_entities(
            Message.id,
            Message.content,
            Message.created_at,
            User.id.label("user_id"),
            User.email.label("user_email"),
            User.first_name.label("user_first_name"),
            User.last_name.label("user_last_name"),
        )
        .filter(Message.lot_id == lot_id)
        .order_by(Message.id.desc())
        .limit(RECENT_MESSAGES_AMOUNT)
    )

    return [
        MessageForDisplay(
            id=message.id,
            lot_id=lot_id,
            content=message.content,
            creation_date=message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            author=UserForDisplay(
                id=message.user_id,
                email=message.user_email,
                first_name=message.user_first_name,
                last_name=message.user_last_name,
            ),
        )
        for message in reversed(query.all())
    ]


def serialize_messages(messages: list[MessageForDisplay]) -> dict:
    return {"messages": messages}


def serialize_new_message(user: User, message: Message) -> dict:
    return serialize_messages(
        [
            MessageForDisplay(
                id=message.id,
                lot_id=message.lot_id,
                content=message.content,
                creation_date=message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                author=UserForDisplay(
                    id=user.id,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                ),
            )
        ]
    )
