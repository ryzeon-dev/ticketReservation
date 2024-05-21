from dao import *
from models import Reservation

def checkReservation(id):
    reservationData = dbExecAndFetch(f'select * from reservation where id={id}')

    if reservationData:
        return Reservation.fromRow(reservationData[0])

def getReservationsFor(id):
    reservationData = dbExecAndFetch(f"select * from reservation where user={id}")

    if reservationData:
        return ( Reservation.fromRow(row) for row in reservationData )