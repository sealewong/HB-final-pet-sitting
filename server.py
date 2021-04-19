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
    """View create new account page."""

    return render_template('new_acct.html')


@app.route('/new_acct/owner')
def new_acct_owner():
    """View create new owner page."""

    return render_template('new_owner.html')


@app.route('/owners', methods=['POST'])
def register_owner():
    """Create a new owner."""
    
    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    address = request.form.get('address')
    payment = request.form.get('payment')        

    owner = crud.get_owner_by_email(email)
        
    if owner:   
        flash('Account already exists. Please log in.')
        return redirect('/login')
    else:    
        owner = crud.create_owner(fname, lname, email, password, address, payment)
        session['email'] = email
        flash('Account created!')
        return redirect('/owner/' + str(owner.owner_id))


@app.route('/new_acct/sitter')
def new_acct_sitter():
    """View create new sitter page."""

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

        return render_template('owner_profile.html', owner=owner, recurring=recurring, short_term=short_term)

    redirect('/login')


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
        return redirect('/sitter/'+ str(sitter.sitter_id))
    else:
        flash('Wrong credentials, please try again')
        return redirect('/login')


@app.route('/sitter/<sitter_id>')
def show_sitter(sitter_id):
    """Show the sitter's profile."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)
        availability = crud.get_availability(sitter_id)
        blockout = crud.get_blockout(sitter_id)

        return render_template('sitter_profile.html', sitter=sitter, availability=availability, blockout=blockout)

    redirect('/login')


@app.route('/owner/<owner_id>/pets')
def show_all_pets(owner_id):
    """View all pets for an owner."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)
        pets = crud.get_all_pets(owner_id)
        
        return render_template('pets.html', owner=owner, pets=pets)

    redirect('/login')


@app.route('/owner/<owner_id>/pets/add_pet_form')  
def add_pet_form(owner_id): 
    """View form to add new pet."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)

        return render_template('add_pet.html', owner=owner)
    
    redirect('/login')


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

    redirect('/login')


@app.route('/owner/<owner_id>/pets/<pet_id>')
def get_pet(owner_id, pet_id):
    """Show details for a pet."""
    
    if 'email' in session:
        pet = crud.get_pet(pet_id)

        return render_template('pet_details.html', pet=pet)

    redirect('/login')


@app.route('/owner/<owner_id>/requests')
def show_all_requests(owner_id):
    """View all sitting requests by owner."""

    if 'email' in session:
        owner = crud.get_owner(owner_id)
        recurrings = crud.get_all_recurrings(owner_id)
        short_terms = crud.get_all_short_terms(owner_id)
        
        return render_template('owner_requests.html', owner=owner, recurrings=recurrings, short_terms=short_terms)

    redirect('/login')


@app.route('/owner/<owner_id>/requests/add_recurring_form')
def add_recurring_form(owner_id):
    """View form to add recurring sitting request."""

    if 'email' in session: 
        owner = crud.get_owner(owner_id)

        return render_template('new_recurring.html', owner=owner)

    redirect('/login')


@app.route('/owner/<owner_id>/requests/add_recurring', methods=['POST'])
def add_recurring(owner_id):
    """Add a new recurring sitting request."""

    time1 = request.form.get('time1')
    time2 = request.form.get('time2')
    time3 = request.form.get('time3')

    if 'email' in session:
        owner = crud.get_owner(owner_id)
        recurring = crud.create_recurring(owner_id, time1, time2, time3)

        return redirect(f'/owner/{owner_id}/requests')

    redirect('/login')


@app.route('/owner/<owner_id>/requests/recurring/<recurring_id>')
def get_recurring(owner_id, recurring_id):
    """Show details for a recurring sitting request."""

    if 'email' in session:
        recurring = crud.get_recurring(recurring_id)

        return render_template('recurring_details.html', recurring=recurring)

    redirect('/login')


@app.route('/owner/<owner_id>/requests/add_short_term_form')
def add_short_term_form(owner_id):
    """View form to add short term sitting request."""

    if 'email' in session: 
        owner = crud.get_owner(owner_id)

        return render_template('new_short_term.html', owner=owner)
    
    redirect('/login')


@app.route('/owner/<owner_id>/requests/add_short_term', methods=['POST'])
def add_short_term(owner_id):
    """Add a new short term sitting request."""

    start = request.form.get('start')
    end = request.form.get('end')
    time1 = request.form.get('time1')
    time2 = request.form.get('time2')
    time3 = request.form.get('time3')

    if 'email' in session:
        owner = crud.get_owner(owner_id)
        short_term = crud.create_short_term(owner_id, start, end, time1, time2, time3)

        return redirect(f'/owner/{owner_id}/requests')
    
    redirect('/login')


@app.route('/owner/<owner_id>/requests/short_term/<short_term_id>')
def get_short_term(owner_id, short_term_id):
    """Show details for a short term sitting request."""

    if 'email' in session:
        short_term = crud.get_short_term(short_term_id)

        return render_template('short_term_details.html', short_term=short_term)

    redirect('/login')


@app.route('/sitter/<sitter_id>/schedules')
def show_all_schedules(sitter_id):
    """View schedules for a sitter."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)
        availabilities = crud.get_all_availability(sitter_id)
        blockouts = crud.get_all_blockouts(sitter_id)

        return render_template('sitter_schedules.html', sitter=sitter, availabilities=availabilities, blockouts=blockouts)

    redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/add_avail_form')
def add_avail_form(sitter_id):
    """View form to add availabilty."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)

        return render_template('new_avail.html', sitter=sitter)

    redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/add_avail', methods=['POST'])
def add_availability(sitter_id):
    """Add a new availability to sitter account."""

    day_of_week = request.form.get('day')
    time_of_day = request.form.get('time')

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)
        availability = crud.create_availability(sitter_id, day_of_week, time_of_day)

        return redirect(f'/sitter/{sitter_id}/schedules')

    redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/avail/<availability_id>')
def get_availability(sitter_id, availability_id):
    """Show details for sitter availability."""

    if 'email' in session: 
        availability = crud.get_availability(availability_id)

        return render_template('avail_details.html', availability=availability)

    redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/add_blockout_form')
def add_blockout_form(sitter_id):
    """View form to add sitter blockout."""

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)

        return render_template('new_blockout.html', sitter=sitter)

    redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/add_blockout', methods=['POST'])
def add_blockout(sitter_id):
    """Add a new blockout to sitter account."""

    start = request.form.get('start')
    end = request.form.get('end')

    if 'email' in session:
        sitter = crud.get_sitter(sitter_id)
        blockout = crud.create_blockout(sitter_id, start, end)

        return redirect(f'/sitter/{sitter_id}/schedules')

    redirect('/login')


@app.route('/sitter/<sitter_id>/schedules/blockout/<blockout_id>')
def get_blockout(sitter_id, blockout_id):
    """Show details for a sitter blockout."""

    if 'email' in session:
        blockout = crud.get_blockout(blockout_id)

        return render_template('blockout_details.html', blockout=blockout)

    redirect('/login')


# @app.route('sitter/<sitter_id>/logout')


# @app.route('owner/<owner_id>/logout')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
