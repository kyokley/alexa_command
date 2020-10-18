from shutdown import shutdown
from flask import Flask, request

app = Flask(__name__)


@app.route('/mercury', methods=['GET', 'POST'])
def mercury():
    if request.method == 'POST':
        try:
            shutdown()
            return 'Success', 200
        except Exception:
            return 'FAIL', 400
    elif request.method == 'GET':
        return 'Shutdown server is listening', 200


if __name__ == '__main__':
    app.run(debug=False)
