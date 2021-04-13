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


@app.route('/login')
def login():
    """Log into existing account."""

    return render_template('login.html')


@app.route('/login/owner', methods=['POST'])
def login_owner():
    
    print(request.form) 

    email = request.form.get("email")
    password = request.form.get("password")
    owner = crud.get_owner_by_email(email)
    print("dugan")
    print(request)
    print(email)
    print(password)

    if owner == None:
        return redirect("/")
        
    elif owner.password == password: 
        session['email'] = email
        return redirect("/owner/" + str(owner.owner_id))


@app.route('/login/sitter')
def sitter_login():
    """Log into existing sitter account."""

    email = request.form.get("email")
    password = reguest.form.get("password")
    sitter = crud.get_sitter_by_email(email)

    return render_template('.html')


@app.route('/newacct')
def new_acct():
    """Create new account."""

    return render_template('signup.html')


@app.route('/owner/<owner_id>')
def show_owner(owner_id):
    """Show a particular owner's profile."""

    if "email" in session:
        owner = crud.get_owner(owner_id)
        recurring = crud.get_recurring(owner_id)
        short_term = crud.get_short_term(owner_id)

        return render_template('owner_profile.html', owner=owner, recurring=recurring, short_term=short_term)

    redirect("/login")


@app.route('/owner/<owner_id>/pets')
def all_pets(owner_id):
    """View all pets for a particular owner."""

    # email log in has to match email for the owner id 

    if "email" in session:
        owner=crud.get_owner(owner_id)
        if owner.email == session["email"]:
            pets = crud.get_all_pets(owner_id)
            return render_template('pets.html', pets=pets)
        else: 
            redirect("/error")

    redirect("/login")

@app.route('/error')
def error_page():
    """View error page."""

    return render_template('error_page.html')


# @app.route('owner/<owner_id>/pets/add')
# def add_pet(owner_id):
# #parse form data to get data for pet
    

#     pet = crud.create_pet(owner_id=owner_id, name=name, species=species, diet=diet, 
#     instructions=instructions)
    

#     return redirect to show pet details 


@app.route('/owner/<owner_id>/pets/<pet_id>')
def get_pet(owner_id, pet_id):
    """Show details for a particular pet."""

    if "email" in session:
        pet = crud.get_pet(pet_id)
        return render_template('pet_details.html', pet=pet)



# @app.route('/owner/<owner_id>/requests')
# def show_owner(owner_id):
#     """Show a particular owner's pet sitting requests."""


# @app.route('/sitter/<sitter_id>')
# def show_sitter(sitter_id):
#     """Show a particular sitter's profile."""


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
