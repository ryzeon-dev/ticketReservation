from dbi import *
from models import User
from hashlib import sha256

def checkUser(uname, passwd, hashedPasswd=False):
    if not hashedPasswd:
        passwd = sha256(passwd.encode()).hexdigest()

    query = f"select * from user where username='{uname}' and password='{passwd}';"
    userData = dbExecAndFetch(query)

    if userData:
        user = User.fromRow(userData[0])
        userToken = dbExecAndFetch(f"select token from token where user={user.id};")

        if userToken:
            user.token = userToken[0][0]

        return user

def getUser(username):
    user = dbExecAndFetch(f"select * from user where username='{username}'")

    if user:
        return User.fromRow(user[0])

def registerUser(name, username, password):
    passwordHash = sha256(password.encode()).hexdigest()

    db = DB()
    db.exec(f"insert into user (name, username, password, creator) values ('{name}', '{username}', '{passwordHash}', false);")

    db.commit()
    db.close()

def getUserBy(id):
    user = dbExecAndFetch(f'select * from user where id={id}')

    if user:
        return User.fromRow(user[0])

def listUsers():
    users = dbExecAndFetch('select * from user;')

    if users:
        return (User.fromRow(row) for row in users)