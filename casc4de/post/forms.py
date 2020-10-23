from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            DataRequired(), 
            Length(min=4, max=200)
        ]
    )
    abstract = TextAreaField(
        "Abstract",
        validators=[
            DataRequired(),
            Length(max=300, message="Maximum 300 characters")
        ]
    )
    cate_id = SelectField(
        "Category",
        coerce=int,
        validators=[
        ]
    )
    content = TextAreaField(
        "Content",
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField("Public")