import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["FootballDBMongo"]

print("Herzlich Willkommen")
userInputClub = input("----------Enter the name of the club---------: ")

query1 = {"name": userInputClub}
query2 = {"TitlesWon": 1, "_id" : 0}

databaseCollection = mydb.clubStats.find(query1,query2)

hasValue = True if mydb.clubStats.count_documents({"name":userInputClub}) > 0 else False

if hasValue:
    for titles in mydb.clubStats.find({"name":userInputClub},{"TitlesWon": 1, "_id" : 0}):
        print("          Number of titles won by the club are/is:")
        print("          Year              Title")
        title = titles["TitlesWon"]
        for k in title:
            for a in k:    
                print("          {}    ".format(k[a]),end="")
            print()
                   
else:
    print("No data found")

