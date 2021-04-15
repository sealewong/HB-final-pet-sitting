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


# @app.route('/owner/<owner_id>/pets')
# def all_pets(owner_id):
#     """View all pets for a particular owner."""

#     # email log in has to match email for the owner id 

#     if "email" in session:
#         owner=crud.get_owner(owner_id)
#         if owner.email == session["email"]:
#             pets = crud.get_all_pets(owner_id)
#             return render_template('pets.html', pets=pets)
#         else: 
#             redirect("/error")

#     redirect("/login")


# @app.route('owner/<owner_id>/pets/add')
# def add_pet(owner_id):
# #parse form data to get data for pet
    

#     pet = crud.create_pet(owner_id=owner_id, name=name, species=species, diet=diet, 
#     instructions=instructions)
    

#     return redirect to show pet details 


# @app.route('/owner/<owner_id>/pets/<pet_id>')
# def get_pet(owner_id, pet_id):
#     """Show details for a particular pet."""

#     if "email" in session:
#         pet = crud.get_pet(pet_id)
#         return render_template('pet_details.html', pet=pet)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
