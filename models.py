import dataclasses

@dataclasses.dataclass
class Date:
    day: int
    month: int
    year: int

    @staticmethod
    def fromString(date):
        chunks = date.split('-')

        return Date (
            day=chunks[2],
            month=chunks[1],
            year=chunks[0]
        )

    def toString(self):
        return f'{self.day}/{self.month}/{self.year}'

@dataclasses.dataclass
class Event:
    id: int
    title: str
    description: str
    price: float
    date: Date

    @staticmethod
    def fromRow(row):
        return Event(
            id=row[0],
            title=row[1],
            description=row[2],
            price=row[4],
            date=Date.fromString(row[3])
        )

    def toJson(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description': self.description,
            'date' : self.date.toString(),
            'price' : self.price
        }

@dataclasses.dataclass
class Reservation:
    id: int
    event: int
    user: int

    @staticmethod
    def fromRow(row):
        return Reservation (
            id=row[0],
            event=row[1],
            user=row[2]
        )

@dataclasses.dataclass
class User:
    id: int
    name: str
    username: str
    password: str
    reservations: list = dataclasses.field(default_factory=lambda: [])
    token: str = None

    @staticmethod
    def fromRow(row):
        return User (
            id=row[0],
            name=row[1],
            username=row[2],
            password=row[3]
        )

    def setToken(self, token):
        self.token = token

    def addReservation(self, reservation):
        self.reservations.append(reservation)

    def toJson(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'username' : self.username
        }