import requests
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    response = requests.get('http://127.0.0.1:1235')
    return response.text
    # return 'Hello, World!'

app.run(host="0.0.0.0", port=1234, debug=True)