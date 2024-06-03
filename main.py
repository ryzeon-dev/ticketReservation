import time
from flask import Flask, request, render_template, redirect
from dbi import *
from models import *
from loginToken import *
from event import *
from reservation import *
from user import *
from hashlib import sha256

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
    if request.method == 'GET':
        return render_template('login.html', register=True, error=None)

    if request.method == 'POST':
        username = request.form['username']

        try:
            askingForToken = request.form['ask-for-token']
        except:
            askingForToken = None
            password =  request.form['password']

        try:
            createEvent = request.form['create-event']
        except:
            createEvent = None

        if askingForToken:
            token = createNewToken()
            user = getUser(username)

            registerToken(token, user.id)
            reservations = getPrettyReservationsFor(user.id)

            return render_template(
                'personalArea.html', id=user.id, name=user.name,
                username=user.username, token=token, reservations=reservations
            )

        if createEvent:
            username = request.form['username']
            title = request.form['title']

            description = request.form['description']
            price = request.form['price']

            places = request.form['places']
            date = request.form['date']

            user = getUser(username)
            reservations = getPrettyReservationsFor(user.id)

            if dbExecAndFetch(f"select * from event where title='{title}'"):
                return render_template(
                    'personalArea.html', id=user.id, name=user.name,
                    username=user.username, token=tokenFor(user.id), reservations=reservations,
                    admin=user.admin, eventMessage=f'Impossible to create event with title "{title}", it already exists'
                )

            else:
                db = DB()
                db.exec(
                    f"insert into event (title, description, event_date, price, places, places_left) values ('{title}', '{description}', '{date}', {price}, {places}, {places})")
                id = db.exec(f"select id from event where title='{title}' and event_date='{date}'")[0][0]
                db.close()

                return render_template(
                    'personalArea.html', id=user.id, name=user.name,
                    username=user.username, token=tokenFor(user.id), reservations=reservations,
                    admin=user.admin, eventMessage=f'Event created with id "{id}"'
                )

        hashing = sha256()
        hashing.update(password.encode())
        passwdHash = hashing.hexdigest()

        user = checkUser(username, passwdHash)
        if user is None:
            return render_template('login.html', register=True, error='Invalid credentials')

        else:
            reservations = getPrettyReservationsFor(user.id)

            return render_template(
                'personalArea.html', id=user.id, name=user.name,
                username=user.username, token=tokenFor(user.id), reservations=reservations, admin=user.admin
            )

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
            listUsersRequest = request.form['list-users']
        except:
            listUsersRequest = None

        if listUsersRequest:
            users = listUsers()
            return render_template(
                'admin.html', id=user.id, name=user.name,
                username=user.username, token=tokenFor(user.id), users=users,
                adminUsername='master', adminPassword='admin'
            )

        try:
            toggleAdmin = request.form['toggle-admin']
        except:
            toggleAdmin = None

        if toggleAdmin:
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

        name = request.form['name']
        if not name:
            return render_template('register.html', error='No name provided')

        username = request.form['username']
        if not username:
            return render_template('register.html', error='No username provided')

        password = request.form['password']
        if not password:
            return render_template('register.html', error='No password provided')

        passwordConfirmation = request.form['confirm-password']
        if not passwordConfirmation:
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

@app.route('/api/list-events/<fromDate>&<toDate>', methods=['GET', 'POST'])
@app.route('/api/list-events/', methods=['GET', 'POST'])
def listEventsAPI(fromDate=None, toDate=None):
    if fromDate is None and toDate is None:
        query = f"SELECT * from event;"

        events = dbExecAndFetch(query)
        return {
            'status' : 'ok',
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

@app.route('/api/new-reservation/', methods=['POST'])
def makeReservationAPI():
    if request.method != 'POST':
        return {
            'status' : 'error',
            'reason' : 'get requests are not allowed'
        }

    token = request.form['token']
    user = checkToken(token)
    if user is None:
        return {
            'status' : 'error',
            'reason' : 'no user associated to token'
        }

    event = checkEvent(request.form['event'])
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

    places = int(request.form['places'])
    if places > event.placesLeft:
        return {
            'status' : 'error',
            'reason' : 'not enough places left'
        }

    paymentAccount = request.form['payment-account']

    db = DB()
    db.exec(f"insert into reservation (event, user, places) values ({event.id}, {user.id}, {places})")

    db.exec(f"update event set places_left={event.placesLeft - int(places)} where event.id={event.id};")
    reservationId = db.exec(f"select id from reservation where event={event.id} and user={user.id}")[0][0]

    db.exec(f"insert into payment (reservation, account, price) values ({reservationId}, '{paymentAccount}', {event.price * int(places)});")
    db.commit()
    db.close()

    return {
        'status' : 'ok',
        'reservation-id' : reservationId
    }

@app.route('/api/check-reservation/', methods=['POST'])
def checkReservationAPI():
    token = request.form['token']
    user = checkToken(token)
    if user is None:
        return {
            'status' : 'error',
            'reason' : 'no user associated to token'
        }

    reservationID = request.form['reservation-id']
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

@app.route('/api/list-reservations/', methods=['POST'])
def listReservationsAPI():
    token = request.form['token']
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

@app.route('/api/create-event/', methods=['POST'])
def createEventAPI():
    token = request.form['token']
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

    title = request.form['title']
    description = request.form['description']
    price = request.form['price']

    date = request.form['date']
    places = request.form['places']

    if dbExecAndFetch(f"select * from event where title='{title}'"):
        return {
            'status' : 'error',
            'reason' : f'event with title "{title}" already exist'
        }

    db = DB()
    db.exec(f"insert into event (title, description, event_date, price, places, places_left) values ('{title}', '{description}', '{date}', {price}, {places}, {places})")
    id = db.exec(f"select id from event where title='{title}' and event_date='{date}'")[0][0]

    db.commit()
    db.close()

    return {
        'status' : 'ok',
        'event-id' : id
    }

@app.route('/api/delete-reservation/', methods=['POST'])
def deleteReservation():
    token = request.form['token']
    reservationID = request.form['reservation-id']

    user = checkToken(token)
    if user is None:
        return {
            'status' : 'error',
            'reason' : 'token not associated with user'
        }

    reservation = checkReservation(reservationID)
    if reservation is None:
        return {
            'status' : 'error',
            'reason' : 'reservation ID does not exist'
        }

    if reservation.user != user.id:
        return {
            'status' : 'error',
            'reason' : 'reservation is not associated with user'
        }

    event = checkEvent(reservation.event)
    now = time.localtime()
    if event.date.year < now.tm_year or \
        (event.date.year == now.tm_year and event.date.month < now.tm_mon) or \
        (event.date.year == now.tm_year and event.date.month == now.tm_mon and event.date.day < now.tm_mday):
        return {
            'status' : 'error',
            'reason' : 'impossible to delete a past reservation'
        }

    paymentAccount = request.form['payment-account']
    if not paymentAccount:
        paymentAccount = dbExecAndFetch(f'select account from payment where reservation={reservationID};')

    db = DB()
    db.exec(f"delete from reservation where id={reservationID};")

    db.exec(f"delete from payment where reservation={reservationID};")
    db.exec(f"update event set places_left={event.placesLeft + reservation.places};")

    db.commit()
    db.close()

    return {
        'status' : 'ok',
        'transfer-account' : paymentAccount
    }

@app.route('/api/update-reservation/', methods=['POST'])
def updateReservation():
    token = request.form['token']
    user = checkToken(token)

    if not user:
        return {
            'status' : 'error',
            'reason' : 'token is not associated with any user'
        }

    reservationID = request.form['reservation-id']
    reservation = checkReservation(reservationID)

    if not reservation:
        return {
            'status' : 'error',
            'reason' : 'reservation does not exist'
        }

    if reservation.user != user.id:
        return {
            'status' : 'error',
            'reason' : 'user not allowed to edit this reservation'
        }

    places = int(request.form['places'])
    if reservation.places == places:
        return {
            'status' : 'alert',
            'problem' : 'no change applied to reservation'
        }

    event = checkEvent(reservation.event)

    paymentAccount = request.form['payment-account']
    alreadyPaid = int(dbExecAndFetch(f'select price from payment where id={reservationID}')[0][0])

    transaction = - (alreadyPaid - places * event.price)
    placesDelta = reservation.places - places

    db = DB()
    db.exec(f'update reservation set places={places} where id={reservationID}')

    db.exec(f'update event set places_left={event.placesLeft + placesDelta} where id={event.id}')
    db.exec(f"insert into payment (reservation, account, price) values ({reservation.id}, '{paymentAccount}', {transaction});")

    db.commit()
    db.close()

    return {
        'status' : 'ok',
        'action' : 'reservation places changed. The transaction will have place on the provided bank account'
    }

@app.route('/api/request-token/', methods=['POST'])
def requestToken():
    username = request.form['username']
    password = request.form['password']

    user = checkUser(username, password)

    if user is None:
        return {
            "status" : "error",
            "reason" : "user does not exist"
        }

    if user.token:
        return {
            "status" : "alert",
            "problem" : "token already assigned to user",
            "token" : user.token
        }

    token = createNewToken()
    registerToken(token, user.id)

    return {
        "status" : "ok",
        "token" : user.token
    }

if __name__ == '__main__':
    app.run()