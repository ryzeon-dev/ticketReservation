from dao import *
from models import Reservation

def checkReservation(id):
    reservationData = dbExecAndFetch(f'select * from reservation where id={id}')[0]

    if reservationData:
        return Reservation.fromRow(reservationData)