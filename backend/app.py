from flask import Flask
from flask_cors import CORS

from routes.user_routes import user_bp
from routes.upload_routes import upload_bp
from routes.analysis_routes import analysis_bp
from routes.chat_routes import chat_bp

print("UPLOAD BP IMPORTED")

app = Flask(__name__)

CORS(
    app,
    origins=["http://localhost:3000"],
    supports_credentials=True
)


app.register_blueprint(user_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(chat_bp)

print(app.url_map)

@app.route("/")
def home():

    return {
        "message":"Backend Running"
    }

if __name__ == "__main__":

    app.run(
        debug=True,
        port=8080
    )