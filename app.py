from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask is running on a local server!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3099, debug=True)
