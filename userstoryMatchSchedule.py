from py2neo import Graph, Node, Relationship
import datetime

def neo4j():
    graphHost='localhost'
    graphUser = "neo4j"
    graphPassphrase = "chinmay007"
    graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)
    return graph

def getMatchSchedule():
    graph=neo4j()
    print("Find the match schedule in a season:")
    club=input("Enter the club name:")
    year=datetime.datetime.now().year-1
    allSeasons=graph.run("match(n:Game {year:'"+str(year)+"'})<-[r:GAME_PLAYED]-(s:Season {name:'Year"+str(year)+"'})  where n.name contains '"+club+"' return n.schedule,n.name")
    for game in allSeasons:
        print(game["n.name"]+" to take place in "+game["n.schedule"])
        
getMatchSchedule()