from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from  wtforms.validators import DataRequired,Email

class RegisterForm(FlaskForm):
    name=StringField('Name:',validators=[DataRequired()])
    email=StringField('Email:',validators=[Email()])
    roll=IntegerField('Regd.No:',validators=[DataRequired()])
    branch=StringField('Branch:')
    sec=StringField('Secion:')
    status=IntegerField('Status:')
    submit=SubmitField('REGISTER')

class DeleteForm(FlaskForm):
    roll=IntegerField('Regd.No:',validators=[DataRequired()])
    submit=SubmitField('DELETE')
    
'''class UpdateForm(FlaskForm):
    def __init__(self,li):
        self.li=li
        for ele in self.li:
                pass'''



