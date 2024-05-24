import requests

URL = 'http://127.0.0.1:5000'

def testNewReservation():
    data = {
        'event' : '2',
        'token' : 'bgDYN9E5aVp4na4ohaZAsWAgM9CCI3M1p80JdQ9HPNsmMcPsoZdCU9jW7JmgyrqQ',
        'places' : '10',
        'payment-account' : '4931567732900761'
    }

    respose = requests.post(f'{URL}/api/new-reservation', data)
    print(respose.text)

def testCheckReservation():
    data = {
        'token' : 'bgDYN9E5aVp4na4ohaZAsWAgM9CCI3M1p80JdQ9HPNsmMcPsoZdCU9jW7JmgyrqQ',
        'reservation-id' : '2'
    }

    response = requests.post(f'{URL}/api/check-reservation/', data)
    print(response.text)

def testListReservations():
    data = {
        'token' : 'bgDYN9E5aVp4na4ohaZAsWAgM9CCI3M1p80JdQ9HPNsmMcPsoZdCU9jW7JmgyrqQ'
    }

    response = requests.post(f'{URL}/api/list-reservations/', data)
    print(response.text)

def testCreateEvent():
    data = {
        'token' : 'to4OTYH0PSLYbTHYZn4PmyWQ0KVQXWXryEzTUjjWkI8UnG6zR4MDbkyM8q1eiw1K',
        'title' : 'test title',
        'description' : 'test description',
        'price' : '3.32',
        'date' : '2024-08-08',
        'places' : '128'
    }

    response = requests.post(f'{URL}/api/create-event', data)
    print(response.text)

if __name__ == '__main__':
    testCreateEvent()