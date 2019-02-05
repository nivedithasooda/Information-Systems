from py2neo import Graph, Node, Relationship

def neo4j():
    graphHost='localhost'
    graphUser = "neo4j"
    graphPassphrase = "chinmay007"
    graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)
    return graph

def findUnbeatenPerformanceInASeason(club,year,graph):
#find games with the club name
    allGames=graph.run("match(n:Game {year:'"+(year)+"'})<--(s:Season {name:'Year"+year+"'}) where n.name contains '"+club+"' return n.name,n.winner")
    listOfGames=[]
    for game in allGames:
        if(game["n.winner"]!=club and game["n.winner"]!=""):
            listOfGames=[]
            break
        listOfGames.append(game["n.name"])
        
    gamesCount=len(listOfGames) 

    if(gamesCount > 0):
            #print year and game
            print("\nSeason with unbeaten performance: Year"+year)
            print("Matches played:")
            for game in listOfGames:
                print(game)
    return gamesCount

def findUnbeatenPerformanceOfAClub():
    graph=neo4j()
    #find all the seasons club has played for or give a year
    print("Find unbeaten side of a Club in a season:")
    club=input("\nEnter the club:")
    allSeasons=graph.run("match(n:Club {name:'"+club+"'})-[r:PARTICIPATED_IN]->(s:Season)  return s.name")
    if(allSeasons.forward()):
        for season in allSeasons:
                year=season["s.name"]
                year =year.replace('Year','')
                gamesCount=findUnbeatenPerformanceInASeason(club,year,graph)
                if(gamesCount <= 0):
                    print("\nThe season "+season["s.name"]+" did not have unbeaten performance by the club\n")                
    else:
        print("Enter a valid club!") 
    
findUnbeatenPerformanceOfAClub()
