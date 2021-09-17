from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired


class APIKeyForm(FlaskForm):
  api_key = StringField('Enter your Notion API key here', validators=[DataRequired()])
  submit = SubmitField('Submit')
  
class SearchForm(FlaskForm):
  page_id = SelectField('select the page where you want the newsmap')
  submit = SubmitField('Submit')