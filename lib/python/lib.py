import requests

URL = 'http://127.0.0.1:5000' #'https://ticketreservation-production.up.railway.app'

def listEvents(fromDate=None, toDate=None):
    if fromDate and toDate:
        return requests.post(f'{URL}/api/list-events/{fromDate}&{toDate}').json()

    return requests.post(f'{URL}/api/list-events/').json()

def newReservation(event, token, places, paymentAccount):
    return requests.post(f'{URL}/api/new-reservation', {
        'event' : str(event),
        'token' : str(token),
        'places' : str(places),
        'payment-account' : str(paymentAccount)
    }).json()

def checkReservation(token, reservationID):
    return requests.post(f'{URL}/api/check-reservation/', {
        'token' : str(token),
        'reservation-id' : str(reservationID)
    }).json()

def listReservations(token):
    return requests.post(f'{URL}/api/list-reservations/', {
        'token' : str(token)
    }).json()

def createEvent(token, title, description, price, date, places):
    return requests.post(f'{URL}/api/create-event/', {
        'token' : str(token),
        'title' : str(title),
        'description' : str(description),
        'price' : str(price),
        'date' : str(date),
        'places' : str(places)
    }).json()

def deleteReservation(token, reservationID, paymentAccount=None):
    return requests.post(f'{URL}/api/delete-reservation/', {
        'token' : str(token),
        'reservation-id' : str(reservationID),
        'payment-account' : str(paymentAccount) if paymentAccount is not None else ''
    }).json()

def updateReservation(token, reservationID, places, paymentAccount):
    return requests.post(f'{URL}/api/update-reservation/', {
        'token' : str(token),
        'reservation-id' : str(reservationID),
        'places' : str(places),
        'payment-account' : str(paymentAccount)
    }).json()