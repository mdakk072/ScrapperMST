from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, BooleanField, SelectField, IntegerField, SubmitField,DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional

# ToDo List Element Form
class TaskCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=255)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[Optional()])
    completed = BooleanField('Completed')
    priority = SelectField('Priority', choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], coerce=int, default=3)
    category = StringField('Category', validators=[Optional(), Length(max=255)])
    time_estimate = IntegerField('Time Estimate (minutes)', validators=[Optional()])
    recurrence = SelectField('Recurrence', choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], validators=[Optional()])
    attachments = TextAreaField('Attachments', validators=[Optional()])
    comments = TextAreaField('Comments', validators=[Optional()])
    status = SelectField('Status', choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('On Hold', 'On Hold'), ('Completed', 'Completed')], default='Not Started')
    reminder_date = DateTimeLocalField('Reminder Date', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    submit = SubmitField('Create Task')

class TaskModifyForm(TaskCreateForm):
    # Since TaskCreateForm already defines all the fields we need,
    # we don't need to redefine them here. This subclass inherits all fields
    # and validators from TaskCreateForm.
    
    # Example of adding an additional field specific to modifying a task, if needed:
    # modification_reason = TextAreaField('Reason for Modification', validators=[Optional()])
    
    # Override the submit button label, if desired
    submit = SubmitField('Update Task')

    # If you need to add any form-specific validation or processing methods, you can do so here.
# ToDo List Element Form
class TaskCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=255)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[Optional()])
    completed = BooleanField('Completed')
    priority = SelectField('Priority', choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], coerce=int, default=3)
    category = StringField('Category', validators=[Optional(), Length(max=255)])
    time_estimate = IntegerField('Time Estimate (minutes)', validators=[Optional()])
    recurrence = SelectField('Recurrence', choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], validators=[Optional()])
    attachments = TextAreaField('Attachments', validators=[Optional()])
    comments = TextAreaField('Comments', validators=[Optional()])
    status = SelectField('Status', choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('On Hold', 'On Hold'), ('Completed', 'Completed')], default='Not Started')
    reminder_date = DateTimeLocalField('Reminder Date', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    submit = SubmitField('Create Task')

class TaskModifyForm(TaskCreateForm):
    # Since TaskCreateForm already defines all the fields we need,
    # we don't need to redefine them here. This subclass inherits all fields
    # and validators from TaskCreateForm.
    
    # Example of adding an additional field specific to modifying a task, if needed:
    # modification_reason = TextAreaField('Reason for Modification', validators=[Optional()])
    
    # Override the submit button label, if desired
    submit = SubmitField('Update Task')

    # If you need to add any form-specific validation or processing methods, you can do so here.
