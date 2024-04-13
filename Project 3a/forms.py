from flask_wtf import FlaskForm, Recaptchafield
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField
)

from datetime import date
from wtforms.fields import DateField
from wtforms.validators import URL, DataRequired, Email, EqualTo, length

class StockForm(FlaskForm):

    symbol = SelectField("Choose Stock Symbol", [DataRequired()],
        choices=[
            ("IBM", "IBM"),
            ("GOOGL", "GOOGL"),
        ]
    )

    chart_type = SelectField("Select Chart Type", [DataRequired()],
        choices=[
            ("1", "1. Bar"),
            ("2", "2. Line")
        ]
    )

    time_series = SelectField("Select Time Series", [DataRequired()],
        choices=[
            ("1", "1. Intraday"),
            ("2", "2. Daily"),
            ("3", "3. Weekly"),
            ("4", "4. monthly")
        ]
    )

    start_date = DateField("Enter Start Date")
    end_date = DateField("Enter End Date")
    submit = SubmitField("Submit")
