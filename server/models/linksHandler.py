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

#========================

def hashUrl(url):
    url = bcrypt.hashpw(url.encode("utf-8"),bcrypt.gensalt())
    url = url[::-1]
    url = url[::8]
    return url

def redirectByType(url,user_id):
    if url[4] == 1:
        return url[1],200
    elif url[4] == 2:
        if user_id == url[5]:
            return url[1],200
        else:
            return "Forbidden",403
    elif url[4] == 3:
        if user_id:
            return url[1],200
        else:
            return "Unauthorized",401
    else:
        return "Not found",404

