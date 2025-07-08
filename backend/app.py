# app.py

from flask import Flask
from flask_cors import CORS
from models import db
import config
from routes import job_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
CORS(app)

app.register_blueprint(job_bp)

# Create DB on first run
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
