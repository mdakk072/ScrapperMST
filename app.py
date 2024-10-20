from scraperMst import create_app
from scraperMst.services import create_database

debug = True
port = 7777
host = '0.0.0.0'
app = create_app()  
if __name__ == '__main__':
    create_database(app)
    app.run(debug=debug, port=port, host=host)