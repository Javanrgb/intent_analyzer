from flask import Flask, render_template, jsonify, request
import processor

app = Flask(__name__)

app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
