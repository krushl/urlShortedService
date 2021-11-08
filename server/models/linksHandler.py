import sqlite3


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
    url = c.execute('''SELECT url FROM Links Where alias_url = :alias_url''',{"alias_url":alias_url}).fetchone()
    return "".join(url)

def getUrlForShort(short_url):
    conn=sqlite_connect()
    c = conn.cursor()
    url = c.execute('''SELECT url FROM Links Where short_url = :short_url''',{"short_url":short_url}).fetchone()
    return "".join(url)