from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('sortpyq', methods=['GET'])
def example_endpoint():
    file_path = 'path/to/your/file.txt'  # Replace with the actual path to your text file

    with open(file_path, 'r') as file:
        contents = file.read()

    return jsonify(contents)

if __name__ == '__main__':
    app.run()
