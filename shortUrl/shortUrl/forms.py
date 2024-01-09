from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, URL

class UrlForm(FlaskForm):
    long_url = URLField('Your long URL:', validators=[DataRequired(), URL()])
    submit = SubmitField('CUT', render_kw={'class': 'btn btn-secondary'})