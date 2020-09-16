from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Car(db.Model):
    """ 
    Declare Car table and its attribute
    """
    __tablename__ = 'Car'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100))
    color = db.Column(db.String(100))
    body_type = db.Column(db.String(100))
    seats = db.Column(db.Integer)
    cost_per_hour = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    reports = relationship("CarReport")
    bookings = relationship("Booking")
    locations = relationship("CarLocation")

    def __init__(self, make=None, color=None, body_type=None, 
                 seats=None, cost_per_hour=0):
        """ Constructor for Car model
        
        :param str make: brand of the car
        :param str color: color of the car
        :param str body_type: body type of car
        :param int seats: number of seat
        :param int cost_per_hour: cost per hour 
        """
        self.make = make
        self.color = color
        self.body_type = body_type
        self.seats = seats
        self.cost_per_hour = cost_per_hour

    @property
    def available(self):
        """ check car avalability
        """
        return not (self.booked or self.fixing)

    @property
    def booked(self):
        """ Check the booking status of car
        """
        return self.bookings and \
                (self.bookings[-1].booked or self.bookings[-1].unlocked)

    @property
    def fixing(self):
        """ check fixing status of car
        """
        return self.reports and not self.reports[-1].fixed

    @property
    def current_location(self):
        if not self.locations:
            return 'undefined'
        return self.locations[-1].location

    def __repr__(self):
        return '<Car %r>' % (self.id)

class CarLocation(db.Model):
    """
    Declare Carlocation table and its attributes
    """
    __tablename__ = 'CarLocation'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('Car.id'))
    location = db.Column(db.String(100))
    creation_time = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, car_id, location=None):
        """ Constructor for the CarLocation
        
        :param int car_id: id of an existing car
        :param str location: location of an existing car
        """
        self.car_id = car_id
        self.location = location

    def __repr__(self):
        return '<CarLocation %r>' % (self.id)

class CarReport(db.Model):
    """ Declare CarReport table and its attribute"""
    __tablename__ = 'CarReport'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('Car.id'))
    fixer_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    fixed = db.Column(db.Boolean, default=False)
    creation_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    update_time = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, car_id):
        """ constructor of CarReport
        """
        self.car_id = car_id

    def setFixer(self, fixer_id):
        """ Set fixer id 
        """
        self.fixer_id = fixer_id

    def setFixed(self, fixed=True):
        """ set fixed id
        """
        self.fixed = fixed

    def __repr__(self):
        return '<CarReport %r>' % (self.id)