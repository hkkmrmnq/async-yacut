from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from . settings import SHORT_ID_MAX_LENGTH, SHORT_ID_PATTERN, URL_MAX_LENGTH


class URLForm(FlaskForm):
    original_link = URLField(
        'Ваша ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректная ссылка'),
            Length(max=URL_MAX_LENGTH)
        ]
    )
    custom_id = StringField(
        'Свой идентификатор',
        validators=[
            Optional(), Regexp(
                SHORT_ID_PATTERN,
                message='Только латиница и цифры, '
                        f'не более {SHORT_ID_MAX_LENGTH} символов.'
            )  # Length(SHORT_ID_MAX_LENGTH)
        ]
    )
    submit = SubmitField('Создать')


class UploadForm(FlaskForm):
    files = MultipleFileField(validators=[FileRequired()])
    submit = SubmitField('Загрузить')
