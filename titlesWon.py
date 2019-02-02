import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["FootballDBMongo"]

print("Herzlich Willkommen")
userInputClub = input("     Enter the name of the club  : ")

query1 = {"name": userInputClub}
query2 = {"TitlesWon": 1, "_id" : 0}

databaseCollection = mydb.clubStats.find(query1,query2)
for titles in databaseCollection:
    print("      Number of titles won by the club are/is:")
    print("          Year              Title")
    for k in titles:
        for a in titles[k]:
            for b in a:
                print("          {}    ".format(a[b]),end="")
            print()

            