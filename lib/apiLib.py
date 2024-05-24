import requests

URL = 'http://127.0.0.1:5000'

def testNewReservation(event, token, places, paymentAccount):
    return requests.post(f'{URL}/api/new-reservation', {
        'event' : str(event),
        'token' : str(token),
        'places' : str(places),
        'payment-account' : str(paymentAccount)
    })

def testCheckReservation(token, reservationID):
    return requests.post(f'{URL}/api/check-reservation/', {
        'token' : str(token),
        'reservation-id' : str(reservationID)
    })

def testListReservations(token):
    return requests.post(f'{URL}/api/list-reservations/', {
        'token' : str(token)
    })

def testCreateEvent(token, title, description, price, date, places):
    return requests.post(f'{URL}/api/create-event', {
        'token' : str(token),
        'title' : str(title),
        'description' : str(description),
        'price' : str(price),
        'date' : str(date),
        'places' : str(places)
    })