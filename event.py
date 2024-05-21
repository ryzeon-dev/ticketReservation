from dao import *
from models import Event

def checkEvent(id):
    eventData = dbExecAndFetch(f'select * from event where id={id}')[0]

    if eventData:
        return Event.fromRow(eventData)

def getAllEvents():
    return ( Event.fromRow(row) for row in dbExecAndFetch('select * from event;') )