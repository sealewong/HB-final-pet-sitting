"""CRUD operations."""

from model import (db, Owner, Pet, Sitter, Transaction, Recurring, Short_term, 
Availability, Blockout, connect_to_db)


def create_owner(fname, lname, email, password, address, payment):
    """Create and return a new owner."""

    owner = Owner(fname=fname, lname=lname, email=email, password=password, 
    address=address, payment=payment)

    db.session.add(owner)
    db.session.commit()

    return owner


def create_pet(owner_id, name, species, diet, instructions):
    """Create and return a new pet for a particular owner."""

    pet = Pet(owner_id=owner_id, name=name, species=species, diet=diet, 
    instructions=instructions)

    db.session.add(pet)
    db.session.commit()

    return pet


def create_sitter(fname, lname, email, password, payment):
    """Create and return a new sitter."""

    sitter = Sitter(fname=fname, lname=lname,email=email, password=password, 
    payment=payment)

    db.session.add(sitter)
    db.session.commit()

    return sitter


def create_transaction(owner_id, sitter_id, short_term_id, recurring_id, price, 
rating_for_owner, comment_for_owner, rating_for_sitter, comment_for_sitter):
    """Create and return a new transaction."""

    transaction = Transaction(owner_id=owner_id, sitter_id=sitter_id, 
    short_term_id=short_term_id, recurring_id=recurring_id, price=price, 
    rating_for_owner=rating_for_owner, comment_for_owner=comment_for_owner, 
    rating_for_sitter=rating_for_owner, comment_for_sitter=comment_for_sitter)

    db.session.add(transaction)
    db.session.commit()

    return transaction


def create_recurring(owner_id, time1, time2, time3):
    """Create and return a new recurring request for an owner."""

    recurring = Recurring(owner_id=owner_id, time1=time1, time2=time2, 
    time3=time3)

    db.session.add(recurring)
    db.session.commit()

    return recurring


def create_short_term(owner_id, start, end, time1, time2, time3):
    """Create and return a new short term request for an owner."""

    short_term = Short_term(owner_id=owner_id, start=start, end=end, 
    time1=time1, time2=time2, time3=time3)

    db.session.add(short_term)
    db.session.commit()

    return short_term


def create_availability(sitter_id, day_of_week, time_of_day):
    """Create and return a new availability for a sitter."""

    availability = Availability(sitter_id=sitter_id, day_of_week=day_of_week, 
    time_of_day=time_of_day)

    db.session.add(availability)
    db.session.commit()

    return availability


def create_blockout(sitter_id, start, stop):
    """Create and return a new blockout for a sitter."""

    blockout = Blockout(sitter_id=sitter_id, start=start, stop=stop)

    db.session.add(blockout)
    db.session.commit()

    return blockout


def get_owner_by_email(owner_email):
    """Return a particular owner's profile by email."""
    print(owner_email)
    print(Owner.query.all())
    return Owner.query.filter(Owner.email == owner_email).first()


def get_owner(owner_id):
    """Return a particular owner's profile by id."""

    return Owner.query.filter(Owner.owner_id == owner_id).first()


def get_all_pets(owner_id):
    """Return all pets for a particular owner."""

    return Pet.query.filter(Pet.owner_id==owner_id).all()


def get_pet(pet_id):
    """Return a particular pet's details."""

    return Pet.query.filter(Pet.pet_id==pet_id).first()


def get_recurring(owner_id):
    """Return recurring sitting request by a particular owner."""

    return Recurring.query.filter(Recurring.owner_id==owner_id).first()


def get_short_term(owner_id):
    """Return short term sitting request by a particular owner."""

    return Short_term.query.filter(Short_term.owner_id==owner_id).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
