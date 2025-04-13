from flask import Flask
from flask_cors import CORS

from summary_api import meeting_api
from routes import api

app = Flask(__name__)
CORS(app)

app.register_blueprint(api, url_prefix='/api') # routes are only reachable at /api/
app.register_blueprint(meeting_api, url_prefix='/api/meetings')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
