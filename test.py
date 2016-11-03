import pymongo

client = pymongo.MongoClient()

db = client.test
coll = db.restaurants

# cursor = db.restaurants.find({
#                           # "borough" : "Brooklyn",
#                             # "cuisine" : "Jewish/Kosher"
#                             "name" : "Mozzarella"})

cursor = db.restaurants.find().sort([
    ("borough", pymongo.ASCENDING),
    ("address.zipcode", pymongo.ASCENDING)
])
for document in cursor:
    print document
    print

keys = ['Sydney', 'San_Francisco', 'Cupertino', 'New York', 'Pune', 'Mumbai', 'Atlanta', 'Bangalore']
for i in xrange(len(keys)):
    print keys[i]