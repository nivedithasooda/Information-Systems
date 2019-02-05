import sys
from py2neo import Graph, Node, Relationship
import pymongo
graphHost='localhost'
graphUser = "neo4j"
graphPassphrase = "test"
graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FootballDBMongo"]
mycol = mydb["clubStats"]

def checkSeasonOver(year):
    for g in graph.run("match(g:Game)-[b:GAME_PLAYED]-(s:Season {name:'Year"+year+"'}) return g.result as result"):
        result = g["result"]
        if(result == ''):
            return False
    return True


def getPoints(club):
    for data in mycol.find({"name":club},{"SeasonPoints":1}):
        points = data["SeasonPoints"]
        for p in points:
            if(p["Year"] == year):
                print("Get points {}".format(p["Points"]))
                return int(p["Points"])

year = sys.argv[1]
flag = checkSeasonOver(year)
if(flag == True):
    listOfClubs = []
    for g in graph.run("match(g:Game {year:'"+year+"'})-[b:GAME_PLAYED]-(s:Season {name:'Year"+year+"'}) return g.name as name"):
        listOfClubs.append(g["name"].split("v/s")[0].strip())
        listOfClubs.append(g["name"].split("v/s")[1].strip())
    listOfClubs = set(listOfClubs)
    print(listOfClubs)
    clubPoints = []
    for club in listOfClubs:
        points = getPoints(club)
        print("Points are {}".format(points))
        clubPoints.append((club,points))
    maxPoints = ()
    for x in clubPoints:
        if(maxPoints == ()):
            maxPoints = x
            print(maxPoints)
        else:
            if(maxPoints[1] < x[1]):
                maxPoints = x
    
    for x in mycol.find({"name":maxPoints[0]},{"TitlesWon":1}):
        title = x["TitlesWon"]
        for t in title:
            if(t["year"] == year):
                if(t["TrophyName"]!="EPL"):
                    if(t["TrophyName"]==""):

                        t["TrophyName"] = 'EPL'
        
        mycol.find_one_and_update({"name":maxPoints[0]},{"$set":{"TitlesWon":title}})
        print("The winner of the championship is {}".format(maxPoints[0]))



