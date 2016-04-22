from main import start_up
from flask import (Flask,
                   request,
                   )
from settings import ALEXA_AUTH

app = Flask(__name__)

@app.route('/mercury', methods=['POST'])
def mercury():
    data = request.get_json()
    if data['pass'] == ALEXA_AUTH:
        start_up()
        return 'Success', 200
    else:
        return 'FAIL', 400

if __name__ == '__main__':
    app.run(debug=True)
