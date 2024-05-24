from dbd import *
from models import User
from hashlib import sha256

def checkUser(uname, passwd):
    query = f"select * from user where username='{uname}' and password='{passwd}';"
    print(query)
    userData = dbExecAndFetch(query)

    if userData:
        return User.fromRow(userData[0])

def getUser(username):
    user = dbExecAndFetch(f"select * from user where username='{username}'")

    if user:
        return User.fromRow(user[0])

def registerUser(name, username, password):
    hasing = sha256()
    hasing.update(password.encode())
    passwordHash = hasing.hexdigest()

    db = DB()
    db.exec(f"insert into user (name, username, password) values ('{name}', '{username}', '{passwordHash}');")
    db.close()

def getUserBy(id):
    user = dbExecAndFetch(f'select * from user where id={id}')

    if user:
        return User.fromRow(user[0])

def listUsers():
    users = dbExecAndFetch('select * from user;')

    if users:
        return (User.fromRow(row) for row in users)
