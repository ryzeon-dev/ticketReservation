from dbi import *
import random
from models import User

CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def createNewToken():
    activeTokens = tuple(tok[0] for tok in  dbExecAndFetch('SELECT token from token;'))

    while True:
        token = ''.join(random.choices(CHARS, k=64))

        if token not in activeTokens:
            break

    return token

def registerToken(token, user):
    db = DB()
    db.exec(f"insert into token (user, token) values ({user}, '{token}')")
    db.close()

def checkToken(token):
    userData = dbExecAndFetch(f"select u.* from user u join token t on u.id=t.user where token='{token}';")

    if userData:
        user = User.fromRow(userData[0])

        user.setToken(token)
        return user 

def tokenFor(userID):
    tokenData = dbExecAndFetch(f"select token from token where user={userID}")

    if tokenData:
        return tokenData[0][0]


if __name__ == '__main__':
    createNewToken()