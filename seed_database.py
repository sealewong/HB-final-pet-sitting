"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime, date, time

import crud
import model
import server

os.system('dropdb pets')
os.system('createdb pets')

model.connect_to_db(server.app)
model.db.create_all()

seale = crud.create_owner(fname="Seale", lname="Wong", email="seale.wong@aol.com", 
password="pw123", address="123 Fake Street", payment=25)
tina = crud.create_owner(fname="Tina", lname="Haiser", email="thaiser@yahoo.com", 
password="123password", address="456 Another Lane", payment=45)

dugan = crud.create_pet(owner_id=1, name="Dugan", species="cat", 
diet="wet and dry", instructions="feed twice daily")
hazel = crud.create_pet(owner_id=2, name="Hazel", species="dog", 
diet="dry", instructions="feed twice daily")
tamu = crud.create_pet(owner_id=2, name="Tamu", species="dog", 
diet="dry", instructions="feed twice daily")

diana = crud.create_sitter(fname="Diana", lname="Wong", email="dwong@hotmail.com", 
password="fakepw", payment=25)
patricia = crud.create_sitter(fname="Patricia", lname="Wheeler", 
email="pwheeler@gmail.com", password="password2", payment=40)



