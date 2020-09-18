from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Booking(db.Model):
    """
    This class is the model of Booking record
    """
    __tablename__ = 'Booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('Car.id'))
    duration = db.Column(db.Integer)
    actions = relationship("BookingAction")
    user = relationship("User")
    car = relationship("Car")

    def __init__(self, user_id, car_id, duration=0):
        """
        Constructor of the Booking class

        :param int user_id: id of existing user
        :param int car_id: id of the existing car
        :param int duration: rent duration
        """
        self.user_id = user_id
        self.car_id = car_id
        self.duration = duration

    @property
    def booked(self):
        return self.actions and self.actions[-1].action == "created"

    @property
    def unlocked(self):
        return self.actions and self.actions[-1].action == "unlocked"

    def __repr__(self):
        return '<Booking %r>' % (self.id)

class BookingAction(db.Model):
    """
    This class is the model of BookingAction record
    """
    __tablename__ = 'BookingAction'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('Booking.id'))
    action = db.Column(db.String(100))
    creation_time = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, booking_id, action=None):
        """
        Constructor of BookingAction class

        :param int booking_id: id of existing booking record
        :param str action: action of the user
        """
        self.booking_id = booking_id
        self.action = action

    def __repr__(self):
        return '<BookingAction %r>' % (self.id)
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Booking(db.Model):
    __tablename__ = 'Booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('Car.id'))
    duration = db.Column(db.Integer)
    actions = relationship("BookingAction")
    user = relationship("User")
    car = relationship("Car")

    def __init__(self, user_id, car_id, duration=0):
        self.user_id = user_id
        self.car_id = car_id
        self.duration = duration

    @property
    def booked(self):
        return self.actions and self.actions[-1].action == "created"

    @property
    def unlocked(self):
        return self.actions and self.actions[-1].action == "unlocked"

    def __repr__(self):
        return '<Booking %r>' % (self.id)
    
    def serialize_with_cols(self, cols):
        data = {c: getattr(self, c) for c in cols}
        return data

class BookingAction(db.Model):
    __tablename__ = 'BookingAction'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('Booking.id'))
    action = db.Column(db.String(100))
    creation_time = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, booking_id, action=None):
        self.booking_id = booking_id
        self.action = action

    def __repr__(self):
        return '<BookingAction %r>' % (self.id)

    def serialize_with_cols(self, cols):
        data = {c: getattr(self, c) for c in cols}
        return data
