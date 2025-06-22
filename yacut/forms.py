from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional, URL


class URLForm(FlaskForm):
    original_link = URLField(
        'Ваша ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректная ссылка')
        ]
    )
    custom_id = StringField(
        'Свой идентификатор',
        validators=[Optional()]
    )
    submit = SubmitField('Создать')


class UploadForm(FlaskForm):
    files = MultipleFileField(validators=[FileRequired()])
    submit = SubmitField('Загрузить')
