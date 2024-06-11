import lib
import json

lib.URL = 'http://127.0.0.1:5000'

apiToken = '0qkbnsOLI0uFdRLvS7TMOPxDAD20kNOCkkuukMMxeyC1Bfze0nu5sV5u7ivXaSR0'

# List all events
events = lib.listEvents()

print(
    f'events = {json.dumps(events, indent=4)}\n'
)

# Create a new reservation
reservation = lib.newReservation(
    event=1,
    token=apiToken,
    places=8,
    paymentAccount='1234567890123456'
)
print(f'{reservation = }\n')

reservationID = reservation['reservation-id']

# Check a reservation
checkReservation = lib.checkReservation(token=apiToken, reservationID=reservationID)

print(
    f'checkReservation = {json.dumps(checkReservation, indent=4)}\n'
)

# Check all reservations for the user
print(
    f'{lib.listReservations(token=apiToken) = }\n'
)

# Update a reservation
print(
    f'''{lib.updateReservation(
    token=apiToken, 
    reservationID=reservationID, 
    places=5, 
    paymentAccount="2345678901234567"
) = }\n'''
)

# Delete a reservation
print(
    f'''{lib.deleteReservation(
    token=apiToken,
    reservationID=reservationID
) = }\n'''
)

# Create an event
createdEvent = lib.createEvent(
    token=apiToken,
    title="Test Event",
    description='Event created during API testing',
    price=15,
    places=50,
    date='2024-08-30'
)

createdEventID = createdEvent['event-id']

print(
    f'{createdEvent = }\n'
)

# List events after creation
events = lib.listEvents()

print(
    f'events = {json.dumps(events, indent=4)}\n'
)

# Delete an event
print(
    f'''{lib.deleteEvent(
    token=apiToken,
    eventID=createdEventID
) = }\n'''
)