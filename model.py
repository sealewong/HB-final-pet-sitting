"""Models for pet sitting app."""

from datetime import datetime, date, time
# now we call date(day=1, month=6, year=2021)
# instead of datetime.date(...)
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


class Owner(db.Model):
    """A pet owner."""

    __tablename__ = "owners"

    owner_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    address = db.Column(db.String)

    pet = db.relationship("Pet", backref = "owners")

    recurring = db.relationship("Recurring", backref = "owners")
    short_term = db.relationship("Short_term", backref = "owners")

    # transactions = a list of Transaction objects

    def __repr__(self):
        return f'<Owner owner_id={self.owner_id} email={self.email}>'


class Pet(db.Model):
    """A pet."""

    __tablename__ = "pets"

    pet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))

    name = db.Column(db.String)
    species = db.Column(db.String)
    diet = db.Column(db.String)
    instructions = db.Column(db.String)

    # owners = a list of Owner objects

    def __repr__(self):
        return f'<Pet pet_id={self.pet_id} name={self.name}>'


class Sitter(db.Model):
    """A pet sitter."""

    __tablename__ = "sitters"

    sitter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    payment = db.Column(db.Integer)

    blockout = db.relationship("Blockout", backref = "sitters")
    availability = db.relationship("Availability", backref = "sitters")

    # transactions = a list of Transaction objects

    def __repr__(self):
        return f'<Sitter sitter_id={self.sitter_id} email={self.email}>'


class Transaction(db.Model):
    """A transaction between owner and sitter."""

    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))
    sitter_id = db.Column(db.Integer, db.ForeignKey("sitters.sitter_id"))
    short_term_id = db.Column(db.Integer, db.ForeignKey("short_terms.short_term_id"))
    recurring_id = db.Column(db.Integer, db.ForeignKey("recurrings.recurring_id"))

    price = db.Column(db.Integer)
    rating_for_owner = db.Column(db.Integer)
    comment_for_owner = db.Column(db.String)
    rating_for_sitter = db.Column(db.Integer)
    comment_for_sitter = db.Column(db.String)

    owner = db.relationship("Owner", backref = "transactions")
    sitter = db.relationship("Sitter", backref = "transactions")
    short_term = db.relationship("Short_term", backref = "transactions")
    recurring = db.relationship("Recurring", backref = "transactions")

    def __repr__(self):
        return f'<Transaction transaction_id={self.transaction_id} price={self.price}>'


class Recurring(db.Model):
    """An owner request for recurring pet sitting."""

    __tablename__ = "recurrings"

    recurring_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))

    day = db.Column(db.String)
    time = db.Column(db.Time)

    # owners = a list of Owner objects
    # transactions = a list of Transaction objects

    def __repr__(self):
        return f'<Recurring recurring_id={self.recurring_id} day={self.day} time={self.time}>'


class Short_term(db.Model):
    """A owner request for short term pet sitting."""

    __tablename__ = "short_terms"

    short_term_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))

    start = db.Column(db.Date)
    end = db.Column(db.Date)
    day = db.Column(db.String)
    time = db.Column(db.Time)

    # owners = a list of Owner objects
    # transactions = a list of Transaction objects

    def __repr__(self):
        return f'<Short_term short_term_id={self.short_term_id} start={self.start} day={self.day} time={self.time}>'


class Availability(db.Model):
    """A sitter's availability."""

    __tablename__ = "availabilities"

    availability_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sitter_id = db.Column(db.Integer, db.ForeignKey("sitters.sitter_id"))

    day_of_week = db.Column(db.String)
    time_of_day = db.Column(db.Time)

    # sitters = a list of Sitter objects

    def __repr__(self):
        return f'<Availability availability_id={self.availability_id} day_of_week={self.day_of_week} time_of_day={self.time_of_day}>'


class Blockout(db.Model):
    """A sitter's blockout for availability."""

    __tablename__ = "blockouts"

    blockout_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sitter_id = db.Column(db.Integer, db.ForeignKey("sitters.sitter_id"))
    
    start = db.Column(db.Date)
    end = db.Column(db.Date)

    # sitters = a list of Sitter objects

    def __repr__(self):
        return f'<Blockout blockout_id={self.recurring_id} start={self.start}>'


def connect_to_db(flask_app, db_uri='postgresql:///pets', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app
    connect_to_db(app)