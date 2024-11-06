from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(100), nullable=False)
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    request = db.relationship('Request', backref='result', uselist=False)
