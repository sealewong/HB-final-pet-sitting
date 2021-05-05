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

seale = crud.create_owner(fname="Seale", lname="Wong", 
email="seale.wong@aol.com", password="pw123", address="123 Fake Street")
tina = crud.create_owner(fname="Tina", lname="Haiser", 
email="thaiser@yahoo.com", password="123password", address="456 Another Lane")

dugan = crud.create_pet(owner_id=1, name="Dugan", species="cat", 
diet="wet and dry", instructions="feed twice daily")
hazel = crud.create_pet(owner_id=2, name="Hazel", species="dog", 
diet="dry", instructions="feed twice daily")
tamu = crud.create_pet(owner_id=2, name="Tamu", species="dog", 
diet="dry", instructions="feed twice daily")

diana = crud.create_sitter(fname="Diana", lname="Wong", 
email="dwong@hotmail.com", password="fakepw", payment=25)
patricia = crud.create_sitter(fname="Patricia", lname="Wheeler", 
email="pwheeler@gmail.com", password="password2", payment=40)
kay = crud.create_sitter(fname="Kay", lname="Kim", email="kayk@aol.com",
password="pwfake", payment=20)
monica = crud.create_sitter(fname="Monica", lname="Cruz", 
email="mcruz@gmail.com", password="pw321", payment=100)
lionel = crud.create_sitter(fname="Lionel", lname="Vital", 
email="lionelv@aol.com", password="pw234", payment=10)

avail1 = crud.create_availability(sitter_id=1, day_of_week="Sunday", 
time_of_day=time(15,0))
avail2 = crud.create_availability(sitter_id=1, day_of_week="Friday", 
time_of_day=time(8,0))
avail3 = crud.create_availability(sitter_id=1, day_of_week="Wednesday", 
time_of_day=time(10,0))
avail4 = crud.create_availability(sitter_id=2, day_of_week="Sunday", 
time_of_day=time(15,0))
avail5 = crud.create_availability(sitter_id=3, day_of_week="Sunday", 
time_of_day=time(15,0))

blockout = crud.create_blockout(sitter_id=1, start=date(2021,5,1), 
end=date(2021,5,31))

recurring1 = crud.create_recurring(owner_id=1, day="Sunday", time=time(15,0))
recurring2 = crud.create_recurring(owner_id=1, day="Monday", time=time(18,30))

short_term1 = crud.create_short_term(owner_id=1, start=date(2021,4,25), 
end=date(2021,4,30), day="Wednesday", time=time(10,0))
short_term2 = crud.create_short_term(owner_id=1, start=date(2021,4,25), 
end=date(2021,5,5), day="Friday", time=time(8,0))
