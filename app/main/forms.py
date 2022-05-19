from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')
    

class BlogForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	description = TextAreaField("Describe your blog",validators=[Required()])
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Add comment',validators=[Required()])
    submit = SubmitField()