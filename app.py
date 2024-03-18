from flask_todolist import app
from flask_todolist.services import create_database,add_mock_tasks_for_each_user

if __name__ == '__main__':
    create_database(app)
    add_mock_tasks_for_each_user(app,40)
    app.run(debug=True, port=8000, host='0.0.0.0')  # Run the app