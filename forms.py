from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    search = StringField('Word to Search', validators=[DataRequired(), Length(min=2, max=20)])

