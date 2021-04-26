"""CRUD operations."""

from model import (db, Owner, Pet, Sitter, Transaction, Recurring, Short_term, 
Availability, Blockout, connect_to_db)


def create_owner(fname, lname, email, password, address):
    """Create and return a new owner."""

    owner = Owner(fname=fname, lname=lname, email=email, password=password, 
    address=address)

    db.session.add(owner)
    db.session.commit()

    return owner


def create_pet(owner_id, name, species, diet, instructions):
    """Create and return a new pet for an owner."""

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


def create_transaction(owner_id, sitter_id, price, 
rating_for_owner=None, comment_for_owner=None, rating_for_sitter=None, comment_for_sitter=None, 
short_term_id=None, recurring_id=None,):
    """Create and return a new transaction."""

    transaction = Transaction(owner_id=owner_id, sitter_id=sitter_id, 
    short_term_id=short_term_id, recurring_id=recurring_id, price=price, 
    rating_for_owner=rating_for_owner, comment_for_owner=comment_for_owner, 
    rating_for_sitter=rating_for_owner, comment_for_sitter=comment_for_sitter)

    db.session.add(transaction)
    db.session.commit()

    return transaction


def create_recurring(owner_id, day, time):
    """Create and return a new recurring request for an owner."""

    recurring = Recurring(owner_id=owner_id, day=day, time=time)

    db.session.add(recurring)
    db.session.commit()

    return recurring


def create_short_term(owner_id, start, end, day, time):
    """Create and return a new short term request for an owner."""

    short_term = Short_term(owner_id=owner_id, start=start, end=end, 
    day=day, time=time)

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


def create_blockout(sitter_id, start, end):
    """Create and return a new blockout for a sitter."""

    blockout = Blockout(sitter_id=sitter_id, start=start, end=end)

    db.session.add(blockout)
    db.session.commit()

    return blockout


def get_owner(owner_id):
    """Return an owner by id."""

    return Owner.query.filter(Owner.owner_id == owner_id).first()


def get_owner_by_email(email):
    """Return an owner by email."""

    return Owner.query.filter(Owner.email == email).first()


def get_all_recurrings(owner_id):
    """Return all recurring sitting requests by owner id."""

    return Recurring.query.filter(Recurring.owner_id==owner_id).all()


def get_recurring(recurring_id):
    """Return a recurring sitting request's details."""

    return Recurring.query.filter(Recurring.recurring_id==recurring_id).first()


def get_all_short_terms(owner_id):
    """Return all short term sitting requests by owner id."""

    return Short_term.query.filter(Short_term.owner_id==owner_id).all()


def get_short_term(short_term_id):
    """Return a short term sitting request's details."""

    return Short_term.query.filter(Short_term.short_term_id==short_term_id).first()


def get_sitter(sitter_id):
    """Return a sitter by id."""

    return Sitter.query.filter(Sitter.sitter_id == sitter_id).first()


def get_sitter_by_email(email):
    """Return a sitter by email."""

    return Sitter.query.filter(Sitter.email == email).first()


def get_all_availability(sitter_id):
    """Return all available schedules for a sitter."""

    return Availability.query.filter(Availability.sitter_id==sitter_id).all()


def get_availability(availability_id):
    """Return an available schedule's details."""

    return Availability.query.filter(Availability.availability_id==availability_id).first()


def get_sitters_by_avail(day_of_week, time_of_day):
    """Return all sitters that are available during weekly specified day and time."""

    return Sitter.query.filter(Sitter.availability.any(day_of_week=day_of_week, time_of_day=time_of_day)).all()


# def get_sitters_by_avail_wi_dates(start, end, day, time):
#     """Return all sitters that are available during specified time period."""

#     return Sitter.query.filter(Sitter.blockout.between()

# def filter_by_blockouts(start_date, end_date, day, time):
#     sitters = get_sitters_by_avail(d, t) #use the above fn!
#     for sitter in sitters:
#         for block in sitter.blockout:
#             if block in #range of dates between start and end date
#                 # break
#             # else
#                 # add them to a results list


def get_all_blockouts(sitter_id):
    """Return all blockouts for a sitter."""

    return Blockout.query.filter(Blockout.sitter_id==sitter_id).all()


def get_blockout(blockout_id):
    """Return a sitter's blockout."""

    return Blockout.query.filter(Blockout.blockout_id==blockout_id).first()


def get_blockout_by_dates(start, end):
    """Return a sitter's blockout by dates."""

    return Blockout.query.filter(Blockout.start==start, Blockout.end==end).first()


def get_all_pets(owner_id):
    """Return all pets for an owner."""

    return Pet.query.filter(Pet.owner_id==owner_id).all()


def get_pet(pet_id):
    """Return a pet's details."""

    return Pet.query.filter(Pet.pet_id==pet_id).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
