from shutdown import shutdown
from flask import Flask

app = Flask(__name__)

@app.route('/mercury', methods=['POST'])
def mercury():
    try:
        shutdown()
        return 'Success', 200
    except:
        return 'FAIL', 400

if __name__ == '__main__':
    app.run(debug=True)
