from dbi import *
from models import Reservation, Event, ReservationPretty

def checkReservation(id):
    reservationData = dbExecAndFetch(f'select * from reservation where id={id}')

    if reservationData:
        return Reservation.fromRow(reservationData[0])

def getReservationsFor(id):
    reservationData = dbExecAndFetch(f"select * from reservation where user={id}")

    if reservationData:
        return ( Reservation.fromRow(row) for row in reservationData )

def getPrettyReservationsFor(id):
    reservationData = dbExecAndFetch(f"select r.id, r.places, e.* from reservation r join event e on r.event = e.id  where user={id}")

    if reservationData:
        reservations = []

        for row in reservationData:
            reservations.append(
                ReservationPretty(
                    id=row[0],
                    places=row[1],
                    event=Event.fromRow(row[2:])
                )
            )

        return reservations