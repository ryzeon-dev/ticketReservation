import time
from flask import Flask, request, render_template, redirect
from dao import *
from models import *
from loginToken import checkToken, createNewToken, registerToken, tokenFor
from event import checkEvent, getAllEvents
from reservation import checkReservation, getReservationsFor, getPrettyReservationsFor
from user import checkUser, getUser, registerUser, listUsers, getUserBy
from hashlib import sha256

PORT = 80 #35275
app = Flask(__name__)

####################
###### CLIENT ######
####################

@app.route('/')
def root():
    with open('./templates/index.html', 'r') as file:
       return file.read()

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        try:
            askingForToken = request.form['ask-for-token']
        except:
            askingForToken = None
            password =  request.form['password']

        if askingForToken:
            token = createNewToken()
            user = getUser(username)

            registerToken(token, user.id)
            reservations = getPrettyReservationsFor(user.id)

            return render_template(
                'personalArea.html', id=user.id, name=user.name,
                username=user.username, token=token, reservations=reservations
            )

        else:
            hashing = sha256()
            hashing.update(password.encode())
            passwdHash = hashing.hexdigest()

            user = checkUser(username, passwdHash)
            if user is None:
                return render_template('login.html', error='Invalid credentials')

            else:
                reservations = getPrettyReservationsFor(user.id)

                return render_template(
                    'personalArea.html', id=user.id, name=user.name,
                    username=user.username, token=tokenFor(user.id), reservations=reservations
                )

    else:
        return render_template('login.html', error=None)

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password =  request.form['password']

        hashing = sha256()
        hashing.update(password.encode())
        passwdHash = hashing.hexdigest()

        user = checkUser(username, passwdHash)
        if user is None:
            return render_template('login.html', error='Invalid credentials')

        if user.username != 'master' and not user.admin:
            return render_template('login.html', error='access denied, unauthorized user')

        try:
            request.form['list-users']

        except:
            pass

        else:
            users = listUsers()
            return render_template(
                'admin.html', id=user.id, name=user.name,
                username=user.username, token=tokenFor(user.id), users=users,
                adminUsername='master', adminPassword='admin'
            )

        try:
            toggleAdmin = request.form['toggle-admin']

        except:
            pass

        else:
            user = getUserBy(toggleAdmin)

            db = DB()
            db.exec(f'update user set admin={"FALSE" if user.admin else "TRUE"} where id={toggleAdmin};')
            db.close()

            return render_template(
                'admin.html', id=user.id, name=user.name,
                username=user.username, token=tokenFor(user.id),
                adminUsername='master', adminPassword='admin'
            )

        return render_template(
            'admin.html', id=user.id, name=user.name,
            username=user.username, token=tokenFor(user.id),
            adminUsername='master', adminPassword='admin'
        )


    return render_template('login.html')

@app.route('/list-events/')
def listEvents():
    events = getAllEvents()

    return render_template('listEvents.html', events=events)

@app.route('/api-calls/')
def apiCalls():
    return render_template('apiCalls.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
        except:
            return render_template('register.html', error='No name provided')

        try:
            username = request.form['username']
        except:
            return render_template('register.html', error='No username provided')

        try:
            password = request.form['password']
        except:
            return render_template('register.html', error='No password provided')

        try:
            passwordConfirmation = request.form['confirm-password']
        except:
            return render_template('register.html', error='No passowrd confirmation provided')

        if password != passwordConfirmation:
            return render_template('register.html', error='Password and confirmation are different')

        if getUser(username):
            return render_template('register.html', error=f'User "{username}" already exists')

        registerUser(name, username, password)

        return render_template('goToHome.html', message='Account created succesfully')

    else:
        return render_template('register.html', error=None)

#################
###### API ######
#################

@app.route('/api/list-events/<fromDate>&<toDate>')
@app.route('/api/list-events/')
def listEventsAPI(fromDate=None, toDate=None):
    if fromDate is None and toDate is None:
        query = f"SELECT * from event;"

        events = dbExecAndFetch(query)
        return {
            'events': [Event.fromRow(row).toJson() for row in events]
        }

    if '/' in fromDate:
        fromDate = '-'.join(fromDate.split('/')[::-1])

    if '/' in toDate:
        toDate = '-'.join(toDate.split('/')[::-1])

    query = f"SELECT * from event where date(event_date) >= date('{fromDate}') and date(event_date) <= date('{toDate}');"

    events = dbExecAndFetch(query)
    return {
        'events' : [Event.fromRow(row).toJson() for row in events]
    }

@app.route('/api/new-reservation/event=<event>/token=<token>/places=<places>/payment_account=<paymentAccount>')
def makeReservationAPI(token, event, places, paymentAccount):
    user = checkToken(token)
    if user is None:
        return {
            'status' : 'error',
            'reason' : 'no user associated to token'
        }

    event = checkEvent(event)
    if event is None:
        return {
            'status' : 'error',
            'reason' : 'event does not exist'
        }

    now = time.gmtime()
    if event.date.year < now.tm_year or \
        (event.date.year == now.tm_year and event.date.month < now.tm_mon) or \
         (event.date.year == now.tm_year and event.date.month == now.tm_mon and event.date.day < now.tm_mday):
        return {
            'status': 'error',
            'reason': 'cannot make reservation for a past event'
        }

    if int(places) > event.placesLeft:
        return {
            'status' : 'error',
            'reason' : 'not enough places left'
        }

    db = DB()
    db.exec(f"insert into reservation (event, user, places) values ({event.id}, {user.id}, {places})")

    db.exec(f"update event set places_left={event.placesLeft - int(places)} where event.id={event.id};")
    reservationId = db.exec(f"select id from reservation where event={event.id} and user={user.id}")[0][0]

    db.exec(f"insert into payment (reservation, account, price) values ({reservationId}, '{paymentAccount}', {event.price * int(places)});")
    db.close()

    return {
        'status' : 'ok',
        'reservation-id' : reservationId
    }

@app.route('/api/check-reservation/token=<token>/reservation=<reservationID>')
def checkReservationAPI(token, reservationID):
    user = checkToken(token)
    if user is None:
        return {
            'status' : 'error',
            'reason' : 'no user associated to token'
        }

    reservation = checkReservation(reservationID)
    if reservation is None:
        return {
            'status' : 'error',
            'reason' : 'reservation does not exist'
        }

    if reservation.user != user.id:
        return {
            'status' : 'error',
            'reason' : 'user unauthorized to access this reservation'
        }

    event = checkEvent(reservation.event)
    paymentAccount = dbExecAndFetch(f"select account from payment where reservation={reservationID}")[0][0]

    return {
        'status' : 'ok',
        'reservation' : {
            'id' : reservation.id,
            'user' : user.toJson(),
            'event' : event.toJson(),
            'payment_account' : paymentAccount,
            'places' : reservation.places
        }
    }

@app.route('/api/list-reservations/token=<token>/')
def listReservationsAPI(token):
    print(token)
    user = checkToken(token)
    if user is None:
        return {
            'status' : 'error',
            'reason' : 'nouser associated to token'
        }

    reservations = getReservationsFor(user.id)
    if reservations is None:
        reservations = []

    return {
        'user-id' : user.id,
        'reservations' : [
            reservation.id for reservation in reservations
        ]
    }

@app.route('/api/create-event/token=<token>/title=<title>/description=<description>/price=<price>/date=<date>/places=<places>/')
def createEventAPI(token, title, description, price, date, places):
    user = checkToken(token)
    if user is None:
        return {
            'status': 'error',
            'reason': 'no user associated to token'
        }

    if not user.admin:
        return {
            'status': 'error',
            'reason': 'user has not the privilegies to create an event'
        }

    if '/' in date:
        date = '-'.join(date.split('/')[::-1])

    db = DB()
    db.exec(f"insert into event (title, description, event_date, price, places, places_left) values ('{title}', '{description}', '{date}', {price}, {places}, {places})")
    id = db.exec(f"select id from event where title='{title}' and event_date='{date}'")[0][0]
    db.close()

    return {
        'status' : 'ok',
        'event-id' : id
    }

if __name__ == '__main__':
    app.run()