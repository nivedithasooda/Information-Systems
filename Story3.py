import pymongo
import datetime

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["FootballDBMongo"]


print("This query will give the top 2 managers based on your team budget and player base price ")
userInputTeam = input("Enter the team name : ")

clubWhereClause = {
    "name": userInputTeam}
clubSelectKeys= {"Budget": 1, "_id": 0, "manager":1}
year=datetime.datetime.now().year-1
listManagers={}
clubDetail = mydb.clubStats.find_one(clubWhereClause, clubSelectKeys)
if not clubDetail:
    print("Enter a valid club name!")
else:
        managerWhereClause = {"$and": [ 
                               {"Contract.salary": {"$lt": clubDetail["Budget"]},
                               "managerName": {"$ne": clubDetail["manager"]}}
                             ]}

        managerSelectKeys = {"managerName":1,"_id":0}
        managers = mydb.ManagerStats.find(managerWhereClause, managerSelectKeys)
        for manager in managers:
            managerName=manager["managerName"]
            clubWhereClause =  { "manager": managerName
                            }
            clubSelectKeys= {"SeasonPoints": 1, "_id": 0,"name":1}
            seasonPoints = mydb.clubStats.find(clubWhereClause, clubSelectKeys)
            for points in seasonPoints:
                clubName=points["name"]
                for point in points["SeasonPoints"]:
                        if(point["Year"]==str(year)):
                            listManagers[managerName+", managed team "+clubName+" in "+str(year)]=str(point["Points"])
        for key,value in sorted(listManagers.items(),key=lambda kv:kv[1],reverse=True):
            print("\n"+key+".\nTotal points scored by the team in the season:"+value)
