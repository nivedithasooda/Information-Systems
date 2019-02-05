import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["FootballDBMongo"]


print("This query will give the top 5 attackers based on your team budget and player base price ")
userInputTeam = input("Enter the team name : ")

queryString_partOne = {}

queryString_partOne = {"name": userInputTeam}
queryString_partTwo = {"Budget": 1, "_id": 0}

x = mydb.clubStats.find(queryString_partOne, queryString_partTwo)

has_val = True if mydb.clubStats.count_documents({"name": userInputTeam}) > 0 else False

if has_val:

    for firstValue in x:

        for a in firstValue:

            queryString_partThree = {
                "$and": [{"Position": "Attacker"}, {"BasePrice": {"$lt": firstValue[a]}}, {"Team": {"$ne": userInputTeam}}]}

            queryString_partFour = {"Name": 1, "_id": 0, "BasePrice": 1, "Team": 1}

        y = mydb.playerStats.find(queryString_partThree, queryString_partFour)
        sortedList = y.sort("BasePrice", pymongo.DESCENDING)
        listOfDocuments = sortedList.limit(5)
        print("---LIST OF SUITABLE ATTACKERS IN YOUR PRICE RANGE---")
        for eachDocument in sortedList:
            print(eachDocument)

else:
    print("No records found")
