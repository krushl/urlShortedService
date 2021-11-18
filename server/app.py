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


@app.route("/auth/register", methods=["POST"])
def register():
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
    try:
        id = UserHandler.register(login, password_hash)
        access_token = create_access_token(identity=login)
        data = {"user_id": id[0]}
        return jsonify(access_token=access_token, additional_claims=data)
    except Exception as e:
        print(e)


@app.route("/auth/login", methods=["POST"])
def login():
    id = None
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    try:
        password_hash = UserHandler.login(login)[0]
        id = UserHandler.getId(login)
        print(password_hash)
        print(bcrypt.checkpw(password.encode("utf-8"), password_hash))
        if not bcrypt.checkpw(password.encode("utf-8"), password_hash):
            raise Exception('Пользователя с таким паролем не существует')
        data = {"user_id": id[0]}
        access_token = create_access_token(identity=login, additional_claims=data)
        return jsonify(access_token=access_token)
    except Exception as e:
        print(e)
        return {"ok": 300}


@app.route("/kek", methods=["POST"])
@jwt_required()
def kek():
    url = 'https://vk.com'
    shortUrl = linksHandler.hashUrl(url).decode("utf-8")
    type_id = 1
    linksHandler.createLink(url, shortUrl, 1, None)
    return {"ok": 200}


#redirect  1 - public , 2 - private, 3 - authorized
@app.route("/<shortUrl>", methods=["GET"])
@jwt_required(optional=True)
def redirectShort(shortUrl):

    if bool(get_jwt()):
        user_id = get_jwt()['user_id']
    else:
        user_id = None

    response,status = None,None
    if linksHandler.getUrlForAlias(shortUrl):
        url = linksHandler.getUrlForAlias(shortUrl)

        print(user_id)
        response,status = linksHandler.redirectByType(url,user_id)
        print(response)


    elif linksHandler.getUrlForShort(shortUrl):
        url = linksHandler.getUrlForShort(shortUrl)

        print(user_id)
        response,status = linksHandler.redirectByType(url, user_id)
        print(type(response))

    if status == 200:
        return redirect(response)
    else:
        return response

 # 1 - public , 2 - private, 3 - authorized
@app.route("/createShortUrl", methods=["POST"])
@jwt_required(optional=True)
def createShort():
    url = request.json.get("url", None)
    alias_url =request.json.get("alias_url",None)
    type_id = request.json.get("type_id", None)

    if bool(get_jwt()):
        user_id = get_jwt()['user_id']
    else:
        user_id = None

    if url and type_id:
        shortUrl = linksHandler.hashUrl(url).decode("utf-8")
        if alias_url:
            if type_id == 3 and user_id:
                linksHandler.createLinkWithAlias(url,shortUrl,alias_url,type_id,user_id)
                return {"ok": 200}
            elif type_id == 2 and user_id:
                linksHandler.createLinkWithAlias(url, shortUrl, alias_url, type_id, user_id)
                return {"ok": 200}
            elif type_id == 1:
                linksHandler.createLinkWithAlias(url, shortUrl, alias_url, type_id, user_id)
                return {"ok": 200}
            else:
                return {"bad request":400}
        else:
            if type_id == 3 and user_id:
                linksHandler.createLink(url, shortUrl, type_id, user_id)
                return {"ok": 200}
            elif type_id == 2 and user_id:
                linksHandler.createLink(url, shortUrl, type_id, user_id)
                return {"ok": 200}
            elif type_id == 1:
                linksHandler.createLink(url, shortUrl, type_id, user_id)
                return {"ok": 200}
            else:
                return {"bad request":400}

    else:
        return {"bad request":400}

    print(f"{url},{alias_url},{type_id},{user_id}")

    return {"ok": 200}


if __name__ == '__main__':
    app.run()
