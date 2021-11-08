from flask import Flask
from flask import jsonify
from flask import request
import models.UserHandler as UserHandler
import models.linksHandler as linksHandler
import models.createDb as db

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import bcrypt

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "zykov123"
jwt = JWTManager(app)

db.createDb()

@app.route("/register", methods=["POST"])
def register():
    login = request.json.get("login",None)
    password = request.json.get("password",None)
    password_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(10))
    try:
        UserHandler.register(login,password_hash)
    except Exception as e:
        print(e)
    access_token = create_access_token(identity=login)
    return jsonify(access_token=access_token)



@app.route("/login", methods=["POST"])
def login():
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    try:
        password_hash = UserHandler.login(login)
        if not bcrypt.checkpw(password.encode("utf-8"),password_hash):
            raise Exception('Пользователя с таким паролем не существует')
    except Exception as e:
        print(e)
    access_token = create_access_token(identity=login)
    return jsonify(access_token=access_token)

@app.route("/kek",methods=["GET"])
def kek():
    url = linksHandler.getUrlForShort("sdfsdf")
    print(url)
    return{"ok":200}

@app.route("/shortUrl/",methods=["GET"])
def redirectShort():
    return "lel"

@app.route("/createShortUrl",methods=["POST"])
@jwt_required
def createShort():
    url = request.json.get("url",None)
    alias_url =request.json.get("alias_url",None)
    type_id = request.json.get("type_id", None)
    user_id =   request.json.get("user_id", None)
    print(f"{url},{alias_url},{type_id},{user_id}")


    return {"ok":200}

if __name__ == '__main__':
    app.run()