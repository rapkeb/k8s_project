from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'flask front is running'


@app.route('/flask/getTime', methods=['Get'])
def get_time():
    now = datetime.now()
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return f'The current time is: {current_time_str}'


if __name__ == '__main__':
    app.run(debug=True, port=5005)
