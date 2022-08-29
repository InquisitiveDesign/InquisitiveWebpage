from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, SelectField
from wtforms.validators import Length, DataRequired

class UserForm(FlaskForm):
    beamlength = FloatField(label='Beam Length (mm):', validators=[DataRequired()])
    supportnum = SelectField('Number of supports', choices = [1,2], validators=[DataRequired()])
    loadnum = SelectField('Number of loads', choices = [1,2,3,4,5], validators=[DataRequired()])
    beamdata = SubmitField(label='Submit parameters')

class DataForm(FlaskForm):
    supportloc = FloatField(label='in mm', validators=[DataRequired()])
    supporttype = SelectField('Support Type', choices = ['Fixed','Roller','Pin','Spring'], validators=[DataRequired()])
    supportdirec = SelectField('Support Direction', choices = ['Upwards','Downwards'], validators=[DataRequired()])
    loadloc = FloatField(label='in mm', validators=[DataRequired()])
    loadtype = SelectField('Load Type', choices = ['Point','UVL','UDL','Moment'], validators=[DataRequired()])
    loaddirec = SelectField('Load Direction', choices = ['Upwards','Downwards'], validators=[DataRequired()])
    loadvalue = FloatField(label='Load Value (in kN)', validators=[DataRequired()])
    LoadSuppdata = SubmitField(label='Submit data')
