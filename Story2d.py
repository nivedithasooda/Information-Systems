from py2neo import Graph

graphHost = 'localhost'
graphUser = "neo4j"
graphPassphrase = "chinmay007"
graph = Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)

print("--Lets find the biggest win of the season--")
year = input("Enter the year : ")
team = input("Enter the team : ")

allGameResults = graph.run("MATCH (:Season { name: 'Year"+year+"' })-->(Game) WHERE Game.winner= '"+team+"' RETURN " "Game.result, Game.name ")
#has_val = True if len(list(allGameResults)) else False

if allGameResults.forward():
    list = []
    score = {}
    for oneGameResult in allGameResults:
        score[oneGameResult[1]] = oneGameResult[0]
        val = (abs(int((oneGameResult[0])[0]) - int((oneGameResult[0])[2])))
        score[oneGameResult[1]] = val
        list.append(val)

    for key, value in score.items():
        if max(list) == value:
            print(key + " With a goal difference of " + str(value))

else:
    print("No data found")




