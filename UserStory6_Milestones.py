import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["FootballDBMongo"]

#to view highest milestone achieved 
print("------The largest milestone achieved by the club is -------")
milestoneQuery = [{ "$group": { "_id": 0, "max": {"$max" : "$Goal Number" }}}]
databaseCollection = mydb.MilestoneGoals.aggregate(list(milestoneQuery))

for sortedList in databaseCollection:
    print(sortedList["max"])

userInput = input("------Enter Milestone goal of which you wish to see the data:  ")

milestoneDataQuery = {"Goal Number" : int(userInput)}
milestoneDBdata = mydb.MilestoneGoals.find_one(milestoneDataQuery,{"_id":0})

if milestoneDBdata is None:

    print ("            No such milestone exits")
    
else:
    
    print("     Goal Number     Scored By          Playing for          Against                   Minutes")
    print("     {}           {}          {}            {}                   {} ".format(
    milestoneDBdata["Goal Number"],
    milestoneDBdata["Scored By"], milestoneDBdata["Playing for"],
    milestoneDBdata["Against"], milestoneDBdata["Minutes"]))


