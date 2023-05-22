from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/example', methods=['GET'])
def example_endpoint():
    data = {'message': 'This is an example endpoint'}
    return jsonify(data)

if __name__ == '__main__':
    app.run()
