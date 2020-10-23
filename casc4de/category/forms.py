from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class CategoryForm(FlaskForm):
    name = StringField(
        "Category Name",
        validators=[
            DataRequired(), 
            Length(min=4, max=100)
        ]
    )

    abstract = TextAreaField(
        "Abstract",
        validators=[
            DataRequired(),
            Length(max=300, message="Maximum 300 characters")
        ]
    )
    is_child = BooleanField(
        "Is Child?",
        validators=[
        ]
    )
    parent_id = SelectField(
        "Parent Category",
        coerce=int,
        validators=[
        ]
    )
    submit = SubmitField("Save")