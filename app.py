from scraperMst import create_app
from scraperMst.services import create_database
from scraperMst.ipc_listener import start_zmq_listener  # Import the ZMQ listener

debug = True
port = 7777
host = '0.0.0.0'
app = create_app()  
if __name__ == '__main__':
    create_database(app)
    start_zmq_listener()
    app.run(debug=debug, port=port, host=host)