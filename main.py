from flask import Flask, request, render_template, redirect
from dao import *
from models import *
from loginToken import checkToken, createNewToken, registerToken, tokenFor
from event import checkEvent, getAllEvents
from reservation import checkReservation, getReservationsFor, getPrettyReservationsFor
from user import checkUser, getUser, registerUser
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

@app.route('/list-events/')
def listEvents():
    events = getAllEvents()

    return render_template('listEvents.html', events=events)

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

@app.route('/api/new-reservation/event=<event>/token=<token>/payment_account=<paymentAccount>')
def makeReservationAPI(token, event, paymentAccount):
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

    db = DB()
    db.exec(f"insert into reservation (event, user) values ({event.id}, {user.id})")
    reservationId = db.exec(f"select id from reservation where event={event.id} and user={user.id}")[0][0]

    db.exec(f"insert into payment (reservation, account, price) values ({reservationId}, '{paymentAccount}', {event.price});")
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
            'payment_account' : paymentAccount
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

app.run(host='0.0.0.0', port=PORT)