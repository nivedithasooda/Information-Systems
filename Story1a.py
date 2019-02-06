import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["FootballDBMongo"]

userInputTeam = input("--- Enter the Team name ---")

print("--- Enter the formation ---")

numOfDefenders = input("How many defenders do you need?")
numOfAttacker = input("How many attackers do you need?")
numOfMidfielder = input("How many midfielders do you need?")

if numOfDefenders != 0:

    queryString_partOne = {
        "$and": [{"Position": "Defender"}, {"Performance": {"$gt": "0"}}, {"Team": userInputTeam}, {"Fit": "True"}]}
    queryString_partTwo = {"Name": 1, "_id": 0, "Performance": 1, "Position": 1}
    queryString_partThree = "{" " Performance" ":-1}"
    if(mydb.playerStats.count_documents(queryString_partOne) == 0):
        print("Not enough defenders")

    else:

        x = mydb.playerStats.find(queryString_partOne, queryString_partTwo)

        sortedList = x.sort("Performance", pymongo.DESCENDING)
        listOfDocuments = sortedList.limit(int(numOfDefenders))


        print("---LIST OF SUITABLE DEFENDERS---")
        for eachDocument in sortedList:
            print(eachDocument)



if numOfAttacker != 0:

    queryString_partOne = {
        "$and": [{"Position": "Attacker"}, {"Performance": {"$gt": "1"}}, {"Team": userInputTeam}, {"Fit": "True"}]}
    queryString_partTwo = {"Name": 1, "_id": 0, "Performance": 1, "Position": 1}
    queryString_partThree = "{" " Performance" ":-1}"
    if (mydb.playerStats.count_documents(queryString_partOne) == 0):
        print("Not enough midfielders")
    else:

        x = mydb.playerStats.find(queryString_partOne, queryString_partTwo)
        sortedList = x.sort("Performance", pymongo.DESCENDING)
        listOfDocuments = sortedList.limit(int(numOfAttacker))

        print("---LIST OF SUITABLE ATTACKERS---")
        for eachDocument in sortedList:
            print(eachDocument)

if numOfMidfielder != 0:

    queryString_partOne = {
        "$and": [{"Position": "Midfielder"}, {"Performance": {"$gt": "0"}}, {"Team": userInputTeam}, {"Fit": "True"}]}
    queryString_partTwo = {"Name": 1, "_id": 0, "Performance": 1, "Position": 1}
    queryString_partThree = "{" " Performance" ":-1}"
    if (mydb.playerStats.count_documents(queryString_partOne) == 0):
        print("Not enough attackers")
    else:

        x = mydb.playerStats.find(queryString_partOne, queryString_partTwo)
        sortedList = x.sort("Performance", pymongo.DESCENDING)
        listOfDocuments = sortedList.limit(int(numOfMidfielder))

        print("--LIST OF SUITABLE MIDFIELDERS--")
        for eachDocument in sortedList:
            print(eachDocument)
