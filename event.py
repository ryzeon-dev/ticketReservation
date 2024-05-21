from dao import *
from models import Event

def checkEvent(id):
    eventData = dbExecAndFetch(f'select * from event where id={id}')

    if eventData:
        return Event.fromRow(eventData[0])

def getAllEvents():
    return ( Event.fromRow(row) for row in dbExecAndFetch('select * from event;') )