import sqlite3


def sqlite_connect():
    conn = sqlite3.connect("urlshorted.db")
    return conn


def register(login,password):
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute('''INSERT INTO Users (login,password) VALUES(:login,:password) ''',{"login":login,"password":password})
    id = c.execute("""SELECT id FROM Users WHERE login=:login""",{"login":login}).fetchone()
    conn.commit()
    return id

def login(login):
    conn = sqlite_connect()
    c = conn.cursor()
    password = c.execute('''SELECT password FROM Users WHERE login = :login''',{"login":login})
    conn.commit()
    return password

def getId(login):
    conn = sqlite_connect()
    c = conn.cursor()
    id = c.execute('''SELECT id FROM Users WHERE login = :login''', {"login": login}).fetchone()
    conn.commit()
    return id