from flask import Blueprint

from flask import render_template, request
from flask_login import login_required, current_user
from flask_todolist.models import Task
todolist = Blueprint('todolist', __name__)

@todolist.route('/my_todolist')
@login_required
def my_todolist():
    page = request.args.get('page', 1, type=int)
    per_page = 8
    sort_by = request.args.get('sort_by', 'due_date', type=str)
    direction = request.args.get('direction', 'desc', type=str)

    # Define the mapping from sort_by value to model attribute
    sort_attributes = {
        'title': Task.title,
        'due_date': Task.due_date,
        'start_date': Task.start_date,
        'priority': Task.priority,
        'status': Task.status,
        'category': Task.category,
        'time_estimate': Task.time_estimate,
        'reminder_date': Task.reminder_date
    }

    # Determine the sorting direction
    if direction.lower() == 'desc':
        query = Task.query.filter_by(user_id=current_user.get_id()).order_by(sort_attributes[sort_by].desc())
    else:
        query = Task.query.filter_by(user_id=current_user.get_id()).order_by(sort_attributes[sort_by])

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    todos = pagination.items

    return render_template('my_todolist.html', todos=todos, pagination=pagination, sort_by=sort_by, direction=direction)

