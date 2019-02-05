from py2neo import Graph, Node, Relationship
import datetime
import timedelta

def neo4j():
    graphHost='localhost'
    graphUser = "neo4j"
    graphPassphrase = "test"
    graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)
    return graph

def getMatchScheduleBasedOnDate():
    graph=neo4j()
    print("Find the match schedules in a season from a date:")
    date=input("Enter the date(yyyy-mm-dd):")
    format_str = "%Y-%m-%d" # The format
    try:
        fromDate = datetime.datetime.strptime(date, format_str)
        fromDateStr=datetime.datetime.strftime(fromDate,format_str)
        toDate=fromDate + datetime.timedelta(days=120)
        toDateStr=datetime.datetime.strftime(toDate,format_str)
        year=datetime.datetime.now().year-1
        allSeasons=graph.run("match(n:Game {year:'"+str(year)+"'}) where n.schedule > date('"+fromDateStr+"') and n.schedule < date('"+toDateStr+"') return toString(n.schedule) as timing,n.name,n.location")
        if(allSeasons.forward()):
                for game in allSeasons:
                        print("Game "+game["n.name"]+" on "+game["timing"]+" at "+game["n.location"])
        else:
                print("No upcoming matches in the duration!") 
    except:
        print("Invalid date format")

           
def getMatchSchedule():
    graph=neo4j()
    print("Find the match schedule in a season:")
    club=input("Enter the club name:")
    year=datetime.datetime.now().year-1
    allSeasons=graph.run("match(n:Game {year:'"+str(year)+"'})<-[r:GAME_PLAYED]-(s:Season {name:'Year"+str(year)+"'})  where n.name contains '"+club+"' return toString(n.schedule) as schedule,n.name")
    if(allSeasons.forward()):
        for game in allSeasons:
                print(game["n.name"]+" to take place in "+game["schedule"])
    else:
        print("Enter a valid club!") 

getMatchScheduleBasedOnDate()
#getMatchSchedule()
