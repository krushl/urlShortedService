import sqlite3
import bcrypt


#============database============

def sqlite_connect():
    conn = sqlite3.connect("urlshorted.db")
    return conn

def createLinkWithAlias(url,short_url,alias_url,type_id,user_id):
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute('''INSERT INTO Links (url,short_url,alias_url,type_id,user_id) values(:url,:short_url,:alias_url,:type_id,:user_id)''', {"url": url,"short_url":short_url,"alias_url":alias_url,"type_id":type_id,"user_id":user_id})
    conn.commit()

def createLink(url,short_url,type_id,user_id):
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute('''INSERT INTO Links (url,short_url,type_id,user_id) values(:url,:short_url,:type_id,:user_id)''',{"url":url,"short_url":short_url,"type_id":type_id,"user_id":user_id})
    conn.commit()

def getUrlForAlias(alias_url):
    conn = sqlite_connect()
    c = conn.cursor()
    url = c.execute('''SELECT * FROM Links Where alias_url = :alias_url''',{"alias_url":alias_url}).fetchone()
    return url

def getUrlForShort(short_url):
    conn=sqlite_connect()
    c = conn.cursor()
    url = c.execute('''SELECT * FROM Links Where short_url = :short_url''',{"short_url":short_url}).fetchone()
    return url

def deleteLink(short_url,user_id):
    conn = sqlite_connect()
    c = conn.cursor()
    url = c.execute('''DELETE * FROM Links WHERE short_url = :short_url and user_id = user_id and type_id != 1''',{"short_url":short_url,"user_id":user_id}).fetchone()
    conn.commit()
    return url

# def changeDataLink()
#========================

def hashUrl(url):
    url = bcrypt.hashpw(url.encode("utf-8"),bcrypt.gensalt())
    url = url[::-1]
    url = url[::8]
    return url

def redirectByType(url,user_id):
    type_url = url[4]
    user_id_fromDB = url[5]
    if type_url == 1:
        return url[1],200
    elif type_url == 2:
        if user_id == user_id_fromDB:
            return url[1],200
        else:
            return "Forbidden",403
    elif type_url == 3:
        if user_id:
            return url[1],200
        else:
            return "Unauthorized",401
    else:
        return "Not found",404

