import pymongo
import datetime

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["FootballDBMongo"]

print("This query will give the player details ")
userInputTeam = input("Enter the player name : ")

queryString_partOne = {}

queryString_partOne = {"Name": userInputTeam}
queryString_partTwo = {"BasePrice": 1, "_id": 0, "Contract": 1}

allData = mydb.playerStats.find(queryString_partOne, queryString_partTwo)
year = datetime.datetime.now().year-1

has_val = True if mydb.playerStats.count_documents({"Name": userInputTeam}) > 0 else False

if has_val:

    for oneRecord in allData:
            print("-- The current price of the player is :" + oneRecord["BasePrice"])
            for contract in oneRecord["Contract"]:
                if contract["Year"] == str(year):
                    print("-- Salary of the player is : " + contract["Salary"])
                    print("-- Previous clubs are as below")
                print(contract["Team"])
else:
    print("No data found")
