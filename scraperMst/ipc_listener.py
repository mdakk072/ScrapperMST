import threading
import json
from scraperMst.ipc import IPC  # Import your IPC class
from flask import jsonify  # Import jsonify to return JSON from API

DELIMITER = "::"
ipc = IPC()

# Global variables to store the latest statuses
scraper_status_data = {}
profiles_status_data = {}

def start_zmq_listener():
    """Background thread to listen for ZMQ messages."""
    # Initialize the ZMQ subscriber
    ipc.init_subscriber("status", "tcp://localhost:7578")

    def zmq_listener():
        while True:
            message = ipc.receive_published("status")
            if message:
                print(f"Received message: {message[:20]}")
                
                try:
                    topic, data_str = message.split(DELIMITER, 1)
                    data = json.loads(data_str)

                    # Store the data in memory
                    if topic == 'scraper_status':
                        global scraper_status_data
                        scraper_status_data = data
                        print("Updated scraper_status")
                    elif topic == 'profiles_status':
                        global profiles_status_data
                        profiles_status_data = data
                        print("Updated profiles_status")

                except ValueError as e:
                    print(f"Error splitting message: {e}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    
    # Start the listener in a background thread
    zmq_thread = threading.Thread(target=zmq_listener)
    zmq_thread.daemon = True
    zmq_thread.start()

