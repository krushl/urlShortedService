from flask import Flask
from flask import redirect
from flask import jsonify
from flask import request
import models.UserHandler as UserHandler
import models.linksHandler as linksHandler
import models.createDb as db

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager




import bcrypt

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "zykov123"
jwt = JWTManager(app)

db.createDb()

@app.route("/register", methods=["POST"])
def register():
    id=None
    access_token=None
    login = request.json.get("login",None)
    password = request.json.get("password",None)
    password_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(10))
    try:
       id = UserHandler.register(login,password_hash)
       access_token = create_access_token(identity=login)
       data = {"user_id": id[0]}
       return jsonify(access_token=access_token,additional_claims=data)
    except Exception as e:
        print(e)





@app.route("/login", methods=["POST"])
def login():
    id = None
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    try:
        password_hash = UserHandler.login(login)
        id = UserHandler.getId(login)
        if not bcrypt.checkpw(password.encode("utf-8"),password_hash):
            raise Exception('Пользователя с таким паролем не существует')
        data = {"user_id": id[0]}
        access_token = create_access_token(identity=login, additional_claims=data)
        return jsonify(access_token=access_token)
    except Exception as e:
        print(e)


@app.route("/kek",methods=["POST"])
@jwt_required()
def kek():
    url ='https://vk.com'
    shortUrl = linksHandler.hashUrl(url).decode("utf-8")
    type_id=1
    linksHandler.createLink(url,shortUrl,1,None)
    return {"ok":200}

#public redirect
@app.route("/<shortUrl>",methods=["GET"])
def redirectShort(shortUrl):
    url = linksHandler.getUrlForShort(shortUrl)
    return redirect(url)

@app.route("/createShortUrl",methods=["POST"])
@jwt_required()
def createShort():
    url = request.json.get("url",None)
    alias_url =request.json.get("alias_url",None)
    type_id = request.json.get("type_id", None) # 1 - public , 2 - private, 3 - authorized
    user_id = get_jwt()['user_id']
    print(f"{url},{alias_url},{type_id},{user_id}")

    return {"ok":200}

if __name__ == '__main__':
    app.run()