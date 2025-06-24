import random
import re
import string
from datetime import datetime

from yacut import db
from .error_handlers import NotFound, ShortIDException, UnexpectedBehavior
from .settings import (MAX_RETRY_FOR_SHORT_ID_GENERATION, SHORT_ID_MAX_LENGTH,
                       SHORT_ID_PATTERN, SHORT_URL_ID_LENGTH, URL_MAX_LENGTH)

CHARACTERS = string.ascii_letters + string.digits


def get_unique_short_id():
    """Генерирует идентификатор для коротких ссылок."""
    for _ in range(MAX_RETRY_FOR_SHORT_ID_GENERATION):
        short_id = "".join(random.choices(CHARACTERS, k=SHORT_URL_ID_LENGTH))
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id
    raise UnexpectedBehavior(
        'Не удалось сгенерировать уникальный ID после'
        f'{MAX_RETRY_FOR_SHORT_ID_GENERATION} попыток.'
    )


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_ID_MAX_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    @classmethod
    def create(cls, original, short=None):
        if short:
            if not re.match(SHORT_ID_PATTERN, short):
                raise ShortIDException(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if short == 'files' or cls.query.filter_by(
                short=short
            ).first() is not None:
                raise ShortIDException(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
        else:
            short = get_unique_short_id()
        instance = cls(original=original, short=short)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def retrieve_by_short_id(cls, short):
        instance = cls.query.filter_by(short=short).first()
        if instance is None:
            raise NotFound('Указанный id не найден')
        return instance
