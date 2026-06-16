from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return {"message": "Hello from your new backend monorepo!"}

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True, host='127.0.0.1', port=5000)