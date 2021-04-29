"""Server for pet sitting app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/new_acct')
def new_acct():
    """View page to create a new account."""

    return render_template('new_acct.html')


@app.route('/new_acct/owner')
def new_acct_owner():
    """View page to create a new owner account."""

    return render_template('new_owner.html')


@app.route('/owners', methods=['POST'])
def register_owner():
    """Create a new owner."""

    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    address = request.form.get('address')

    owner = crud.get_owner_by_email(email)

    if owner:
        flash('Account already exists. Please log in.')
        return redirect('/login')
    else:
        owner = crud.create_owner(fname, lname, email, password, address)
        session['email'] = email
        flash('Account created!')
        return redirect('/owner/' + str(owner.owner_id))


@app.route('/new_acct/sitter')
def new_acct_sitter():
    """View page to create a new sitter account."""

    return render_template('new_sitter.html')


@app.route('/sitters', methods=['POST'])
def register_sitter():
    """Create a new sitter."""

    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    payment = request.form.get('payment')

    sitter = crud.get_sitter_by_email(email)

    if sitter:
        flash('Account already exists. Please log in.')
        return redirect('/login')
    else:
        sitter = crud.create_sitter(fname, lname, email, password, payment)
        session['email'] = email
        flash('Account created!')
        return redirect('/sitter/' + str(sitter.sitter_id))


@app.route('/login')
def login():
    """View login page."""

    return render_template('login.html')


@app.route('/login/owner', methods=['POST'])
def login_owner():
    """Log in as owner with credentials."""

    email = request.form.get('email')
    password = request.form.get('password')
    owner = crud.get_owner_by_email(email)

    if owner == None:
        flash('Account does not exist')
        return redirect('/new_acct')
    elif owner.password == password:
        session['email'] = email
        flash('Logged In')
        return redirect('/owner/' + str(owner.owner_id))
    else:
        flash('Wrong credentials, please try again')
        return redirect('/login')


@app.route('/owner/<owner_id>')
def show_owner(owner_id):
    """Show the owner's profile."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)
        recurring = crud.get_recurring(owner_id)
        short_term = crud.get_short_term(owner_id)

        return render_template('owner_profile.html', 
                                owner=owner, 
                                recurring=recurring, 
                                short_term=short_term)

    return redirect('/login')
    

@app.route('/login/sitter', methods=['POST'])
def sitter_login():
    """Log in as sitter with credentials."""

    email = request.form.get('email')
    password = request.form.get('password')
    sitter = crud.get_sitter_by_email(email)

    if sitter == None:
        flash('Account does not exist')
        return redirect('/new_acct')
    elif sitter.password == password:
        session['email'] = email
        flash('Logged In')
        return redirect('/sitter/'+ str(sitter.sitter_id))
    else:
        flash('Wrong credentials, please try again')
        return redirect('/login')


@app.route('/sitter/<sitter_id>')
def show_sitter(sitter_id):
    """Show the sitter's profile."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)

        return render_template('sitter_profile.html', sitter=sitter)

    return redirect('/login')


@app.route('/owner/<owner_id>/pets')
def show_all_pets(owner_id):
    """View all pets for an owner."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)
        pets = crud.get_all_pets(owner_id)

        return render_template('pets.html', owner=owner, pets=pets)

    return redirect('/login')


@app.route('/owner/<owner_id>/pets/add_pet_form')
def add_pet_form(owner_id):
    """View form to add new pet."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)

        return render_template('add_pet.html', owner=owner)

    return redirect('/login')


@app.route('/owner/<owner_id>/pets/add', methods=['POST'])
def add_pet(owner_id):
    """Add a new pet for an owner."""

    name = request.form.get('name')
    species = request.form.get('species')
    diet = request.form.get('diet')
    instructions = request.form.get('instructions')

    if 'email' in session:
        owner = crud.get_owner(owner_id)
        pet = crud.create_pet(owner_id, name, species, diet, instructions)

        return redirect(f'/owner/{owner_id}/pets')

    return redirect('/login')


@app.route('/owner/<owner_id>/pets/<pet_id>')
def get_pet(owner_id, pet_id):
    """Show details for a pet."""

    if 'email' in session:
        pet = crud.get_pet(pet_id)

        return render_template('pet_details.html', pet=pet)

    return redirect('/login')


@app.route('/owner/<owner_id>/requests')
def show_all_requests(owner_id):
    """View all sitting requests by owner."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)
        recurrings = crud.get_all_recurrings(owner_id)
        short_terms = crud.get_all_short_terms(owner_id)
        transactions = owner.transactions

        short_term_id_list = []
        for transaction in transactions:
            short_term_id_list.append(transaction.short_term_id)

        recurring_id_list = []
        for transaction in transactions:
            recurring_id_list.append(transaction.recurring_id)

        return render_template('owner_requests.html', 
                                owner=owner, 
                                recurrings=recurrings, 
                                short_terms=short_terms,
                                transactions=transactions,
                                short_term_id_list=short_term_id_list,
                                recurring_id_list=recurring_id_list)

    return redirect('/login')


@app.route('/owner/<owner_id>/requests/add_recurring_form')
def add_recurring_form(owner_id):
    """View form to add recurring sitting request."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)

        return render_template('new_recurring.html', owner=owner)

    return redirect('/login')


@app.route('/owner/<owner_id>/requests/add_recurring', methods=['POST'])
def add_recurring(owner_id):
    """Add a new recurring sitting request."""

    day = request.form.get('day')
    time = request.form.get('time')

    if 'email' in session:
        recurring = crud.create_recurring(owner_id, day, time)

        return redirect(f'/owner/{owner_id}/requests')

    return redirect('/login')


@app.route('/owner/<owner_id>/requests/recurring/<recurring_id>')
def get_recurring(owner_id, recurring_id):
    """Show details for a recurring sitting request and available sitters."""

    if 'email' in session:
        recurring = crud.get_recurring(recurring_id)
        day_of_week = recurring.day
        time_of_day = recurring.time
        sitters = crud.get_sitters_by_avail(day_of_week, time_of_day)

        return render_template('recurring_details.html', 
                                recurring=recurring, 
                                sitters=sitters)

    return redirect('/login')


@app.route('/<sitter_id>/recurring/<recurring_id>/confirm')
def confirm_recurring(sitter_id, recurring_id):
    """Creates a transaction based on an owner's recurring request."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)
        owner = crud.get_owner_by_email(session['email'])
        transaction = crud.create_transaction(owner.owner_id, 
                                              sitter_id, 
                                              sitter.payment, 
                                              recurring_id=recurring_id)

        return redirect(f'/owner/{owner.owner_id}/requests')


@app.route('/owner/<owner_id>/requests/add_short_term_form')
def add_short_term_form(owner_id):
    """View form to add short term sitting request."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)

        return render_template('new_short_term.html', owner=owner)

    return redirect('/login')


@app.route('/owner/<owner_id>/requests/add_short_term', methods=['POST'])
def add_short_term(owner_id):
    """Add a new short term sitting request."""

    start = request.form.get('start')
    end = request.form.get('end')
    day = request.form.get('day')
    time = request.form.get('time')

    if 'email' in session:
        short_term = crud.create_short_term(owner_id, start, end, day, time)

        return redirect(f'/owner/{owner_id}/requests')

    return redirect('/login')


@app.route('/owner/<owner_id>/requests/short_term/<short_term_id>')
def get_short_term(owner_id, short_term_id):
    """Show details for a short term sitting request and available sitters."""

    if 'email' in session:
        short_term = crud.get_short_term(short_term_id)
        start = short_term.start
        end = short_term.end
        day = short_term.day
        time = short_term.time
        sitters = crud.filter_by_blockouts(start, end, day, time)

        return render_template('short_term_details.html', 
                                short_term=short_term, 
                                sitters=sitters)

    return redirect('/login')


@app.route('/<sitter_id>/short_term/<short_term_id>/confirm')
def confirm_short_term(sitter_id, short_term_id):
    """Creates a transaction based on an owner's short term request."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)
        owner = crud.get_owner_by_email(session['email'])
        transaction = crud.create_transaction(owner.owner_id, 
                                              sitter_id, 
                                              sitter.payment, 
                                              short_term_id=short_term_id)

        return redirect(f'/owner/{owner.owner_id}/requests')


@app.route('/sitter/<sitter_id>/schedules')
def show_all_schedules(sitter_id):
    """View schedules for a sitter."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)
        availabilities = crud.get_all_availability(sitter_id)
        blockouts = crud.get_all_blockouts(sitter_id)
        transactions = sitter.transactions

        return render_template('sitter_schedules.html', 
                                sitter=sitter, 
                                availabilities=availabilities, 
                                blockouts=blockouts,
                                transactions=transactions)

    return redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/add_avail_form')
def add_avail_form(sitter_id):
    """View form to add availabilty."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)

        return render_template('new_avail.html', sitter=sitter)

    return redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/add_avail', methods=['POST'])
def add_availability(sitter_id):
    """Add a new availability to sitter account."""

    day_of_week = request.form.get('day')
    time_of_day = request.form.get('time')

    if 'email' in session:
        availability = crud.create_availability(sitter_id, 
                                                day_of_week, 
                                                time_of_day)

        return redirect(f'/sitter/{sitter_id}/schedules')

    return redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/add_blockout_form')
def add_blockout_form(sitter_id):
    """View form to add sitter blockout."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)

        return render_template('new_blockout.html', sitter=sitter)

    return redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/add_blockout', methods=['POST'])
def add_blockout(sitter_id):
    """Add a new blockout to sitter account."""

    start = request.form.get('start')
    end = request.form.get('end')

    if 'email' in session:
        blockout = crud.create_blockout(sitter_id, start, end)

        return redirect(f'/sitter/{sitter_id}/schedules')

    return redirect('/login')


@app.route('/owner/<owner_id>/transactions/<transaction_id>')
def get_transaction(owner_id, transaction_id):
    """Show details for a transaction from owner's side."""

    if 'email' in session:
        transaction = crud.get_transaction(transaction_id)

        return render_template('confirmed_details.html', transaction=transaction)

    return redirect('/login')


@app.route('/sitter/<sitter_id>/transactions/<transaction_id>')
def show_transaction(sitter_id, transaction_id):
    """Show details for a transaction from sitter's side."""

    if 'email' in session:
        transaction = crud.get_transaction(transaction_id)

        return render_template('confirmed_details.html', transaction=transaction)

    return redirect('/login')


@app.route('/sitter/<sitter_id>/logout')
def log_sitter_out(sitter_id):
    """Logs sitter out of their account."""

    session.clear()
    flash('You are signed out.')
    return redirect('/')


@app.route('/owner/<owner_id>/logout')
def log_owner_out(owner_id):
    """Logs owner out of their account."""

    session.clear()
    flash('You are signed out.')
    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
