from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Car(db.Model):
    __tablename__ = 'Car'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100))
    color = db.Column(db.String(100))
    body_type = db.Column(db.String(100))
    seats = db.Column(db.Integer)
    cost_per_hour = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    reports = relationship("CarReport")

    def __init__(self, make=None, color=None, body_type=None, 
                 seats=None, cost_per_hour=0, available=True):
        self.make = make
        self.color = color
        self.body_type = body_type
        self.seats = seats
        self.cost_per_hour = cost_per_hour
        self.available = available

    @property
    def availability(self):
        if self.reports and not self.reports[-1].fixed:
            return "fixing"
        return "yes"

    def __repr__(self):
        return '<Car %r>' % (self.id)

class CarLocation(db.Model):
    __tablename__ = 'CarLocation'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('Car.id'))
    location = db.Column(db.String(100))
    creation_time = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, car_id, location=None):
        self.car_id = car_id
        self.location = location

    def __repr__(self):
        return '<CarLocation %r>' % (self.id)

class CarReport(db.Model):
    __tablename__ = 'CarReport'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('Car.id'))
    fixer_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    fixed = db.Column(db.Boolean, default=False)
    creation_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    update_time = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, car_id):
        self.car_id = car_id

    def setFixer(self, fixer_id):
        self.fixer_id = fixer_id

    def setFixed(self, fixed=True):
        self.fixed = fixed

    def __repr__(self):
        return '<CarReport %r>' % (self.id)