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

    def __init__(self, user_id, car_id, duration=0):
        self.user_id = user_id
        self.car_id = car_id
        self.duration = duration

    def __repr__(self):
        return '<Booking %r>' % (self.id)

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
