from faker import Faker 

fake = Faker() # is this supposed to be faker or fake?

# for _ in range(10):
#     print(fake.random_int(5,50))

# change "price" in sitters to different name from transactions "price"

Faker.seed(5)
for _ in range(5):
    print(fake.date_time_between_dates())

# Faker.seed(0)
# for _ in range(5):
#     print(fake.future_date())

# Faker.seed(0)
# for _ in range(5):
#     print(fake.time())

# Faker.seed(0)
# for _ in range(5):
#     print(fake.day_of_week())

# for _ in range(10):
#     print(fake.profile())

# for _ in range(10):
#     print(fake.first_name())

# for _ in range(10):
#     print(fake.last_name())

# for _ in range(10):
#     print(fake.email())

# for _ in range(10):
#     print(fake.password())

# for _ in range(10):
#     print(fake.address())

# start date and end date: random range of dates?

# Faker.seed(0)
# for _ in range (5):
#     print(fake.random_choices(elements = ("GAIGA", "TOMMI", BRENDA, TOFI, KAILEE, FELONY, YIPPIE, ZOTIA, GAEGOGI, 
# FATHER, BANDERA, BRIANNA, TURBO, RUFO, MOLLYBLOOM, SHINY, CHAYO, BIG-BOY, OLIE, 
# PENDLETON, SURIS, BRITTANY, CHEWCHEW, RYUSHKA, PEPE, JACQUE, SNAILS, TWEE, DON, 
# GROMET, MUENSY, JEANETTE, SHINER, SHANG, LYNX, LAGUNA, RAINE, NIMO, REONA, 
# TIGER, DUSTY-LEE, CHUMLIE, TEDDY, THELO, NAN, SLUG, BISCOTTI, GEORGIE, CUDI, 
# INGA)))

use random.choice instead of faker library

for _ in range(1):
    print(fake.random_choices(elements = ("dog", "cat", "fish", "hamster", "bird", 
    "bunny"), length=1))

