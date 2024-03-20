from flask_todolist import create_app
from flask_todolist.services import create_database,add_mock_tasks_for_each_user

debug = True
port = 5000
host = '0.0.0.0'
app = create_app()  
if __name__ == '__main__':
    app.run(debug=debug, port=port, host=host)