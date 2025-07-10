# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50))
    posting_date = db.Column(db.String(50))  # keeping as string for now
    tags = db.Column(db.String(255))
    description = db.Column(db.Text)
