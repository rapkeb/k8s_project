from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('load_data.html')


@app.route('/welcome')
def welcome():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5005)
