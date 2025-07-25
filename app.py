from flask import Flask
from routes import face_routes

app = Flask(__name__)
app.register_blueprint(face_routes)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
