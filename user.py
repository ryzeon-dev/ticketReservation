from dao import *
from models import User

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