from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
import os
from models import db, Request, Result
from utils import compute_csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret'
db.init_app(app)
jwt = JWTManager(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.before_request
def create_tables():
    db.create_all()


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username == 'user' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401


@app.route('/api/compute', methods=['POST'])
@jwt_required()
def compute():
    user = request.json.get('user', 'unknown')
    name = request.json.get('name', 'unnamed_request')

    if 'file' not in request.files:
        return jsonify({"msg": "No file part in request"}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({"msg": "Only CSV files are accepted"}), 400


    file_path = f"uploads/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True) 
    file.save(file_path)


    try:
        total = compute_csv(file_path)
    except Exception as e:
        return jsonify({"msg": "Error processing file", "error": str(e)}), 400


    result = Result(total=total)
    db.session.add(result)
    db.session.flush()

    req = Request(user=user, name=name, file_path=file_path, result_id=result.id)
    db.session.add(req)
    db.session.commit()

    return jsonify({"total": total})

if __name__ == '__main__':
    app.run(debug=True)
