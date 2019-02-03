import sys
from py2neo import Graph, Node, Relationship
import pymongo
graphHost='localhost'
graphUser = "neo4j"
graphPassphrase = "chinmay007"
graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FootballDBMongo"]
mycol = mydb["playerStats"]




def get_list_of_players(team):
    players = []
    for p in graph.run("match (p:Player)-[b:BELONGS_TO]->(c:Club {name:'"+team+"'}),(p:Player)-[q:PLAYS]->(g:Game {name:'"+home_team+" v/s "+away_team+"'}) return p.name as players"):
        players.append(p["players"])
    print(players)
    return players


def calc_stats(team,players):
    if(" " in team):
        team = team.replace(" ","_")
    
    for p in players:
        graph.run("MATCH (p:Player {name:'"+p+"'})-[q:PLAYS]-(g:Game {name:'"+sys.argv[1].split("_")[0]+" v/s "+sys.argv[1].split("_")[1]+"'}) SET g."+team+"_fouls = g."+team+"_fouls + q.fouls, g."+team+"_totalShots = g."+team+"_totalShots + q.shots, g."+team+"_yellowCards = g."+team+"_yellowCards + q.yellow_cards, g."+team+"_redCards = g."+team+"_redCards + q.red_cards")

def findWinnerAndCalcPerf(home_team,home_players,away_team,away_players):
    home_sum = 0
    away_sum = 0
    perf_home = {}
    perf_away = {}
    for p in home_players:
        player_score = 0
        for g in graph.run("MATCH (p:Player {name:'"+p+"'})-[q:PLAYS]-(g:Game {name:'"+sys.argv[1].split("_")[0]+" v/s "+sys.argv[1].split("_")[1]+"'}) return q.goals as goals, q.assists as assists, q.chances as chances, q.tackles as tackles, q.passes as passes, q.goals_saved as goals_saved, q.yellow_cards as ycards, q.red_cards as rcards, q.in_time as itime, q.out_time as otime"):
            home_sum = home_sum + g["goals"]
            player_score = (1 * g["goals"]) + (0.75 * g["assists"]) + (0.65 * g["chances"]) + (0.5 * g["tackles"]) + (0.25 * g["passes"]) + (0.75 * g["goals_saved"])
            perf_home[p] = player_score
            for x in mycol.find({"Name":p},{"Name":1,"Goals":1,"Saves":1,"Assists":1,"Saves":1,"YellowCards":1,"RedCards":1,"ManOfTheMatch":1,"Tackles":1,"Performance":1,"MinutesPlayed":1,"_id":0}):
                if(x["Performance"] == "0"):
                    x["Performance"] = perf_home[p]
                else:
                    x["Performance"] = (int(x["Performance"]) + perf_home[p])/2
                x["Goals"] = int(x["Goals"]) + g["goals"]
                x["Saves"] = int(x["Saves"]) + g["goals_saved"]
                x["YellowCards"] = int(x["YellowCards"]) + g["ycards"]
                x["RedCards"] = int(x["RedCards"]) + g["rcards"]
                x["RedCards"] = int(x["RedCards"]) + g["rcards"]
                x["Tackles"] = int(x["Tackles"]) + g["tackles"]
     #Need to check for 2017           
                for min in x["MinutesPlayed"]:

                    if(min["year"] == "2018"):

                        min["Minutes"] = int(min["Minutes"]) + (int(g["otime"]) - int(g["itime"]))
                            
                mycol.find_one_and_update({"Name":p},{"$set":{"MinutesPlayed":x["MinutesPlayed"]}})


                newValues = [{"Performance":x["Performance"]},{"Goals":x["Goals"]},{"Saves":x["Saves"]},{"YellowCards":x["YellowCards"]},{"RedCards":x["RedCards"]},{"Tackles":x["Tackles"]}]
                for value in newValues:
                    mycol.find_one_and_update({"Name":p},{"$set":value})
            



    for p in away_players:
        player_score = 0
        for g in graph.run("MATCH (p:Player {name:'"+p+"'})-[q:PLAYS]-(g:Game {name:'"+sys.argv[1].split("_")[0]+" v/s "+sys.argv[1].split("_")[1]+"'}) return q.goals as goals, q.assists as assists, q.chances as chances, q.tackles as tackles, q.passes as passes, q.goals_saved as goals_saved, q.yellow_cards as ycards, q.red_cards as rcards, q.in_time as itime, q.out_time as otime"):
            away_sum = away_sum + g["goals"]
            player_score = (1 * g["goals"]) + (0.75 * g["assists"]) + (0.65 * g["chances"]) + (0.5 * g["tackles"]) + (0.25 * g["passes"]) + (0.75 * g["goals_saved"])
            perf_away[p] = player_score
            for x in mycol.find({"Name":p},{"Name":1,"Goals":1,"Saves":1,"Assists":1,"Saves":1,"YellowCards":1,"RedCards":1,"ManOfTheMatch":1,"Tackles":1,"Performance":1,"MinutesPlayed":1,"_id":0}):
                if(x["Performance"] == "0"):
                    x["Performance"] = perf_away[p]
                else:
                    x["Performance"] = (int(x["Performance"]) + perf_away[p])/2
                x["Goals"] = int(x["Goals"]) + g["goals"]
                x["Saves"] = int(x["Saves"]) + g["goals_saved"]
                x["YellowCards"] = int(x["YellowCards"]) + g["ycards"]
                x["RedCards"] = int(x["RedCards"]) + g["rcards"]
                x["RedCards"] = int(x["RedCards"]) + g["rcards"]
                x["Tackles"] = int(x["Tackles"]) + g["tackles"]

                for min in x["MinutesPlayed"]:
    
                    if(min["year"] == "2018"):

                        min["Minutes"] = int(min["Minutes"]) + (int(g["otime"]) - int(g["itime"]))
                            
                mycol.find_one_and_update({"Name":p},{"$set":{"MinutesPlayed":x["MinutesPlayed"]}})

                newValues = [{"Performance":x["Performance"]},{"Goals":x["Goals"]},{"Saves":x["Saves"]},{"YellowCards":x["YellowCards"]},{"RedCards":x["RedCards"]},{"Tackles":x["Tackles"]}]
                for value in newValues:
                    mycol.find_one_and_update({"Name":p},{"$set":value})

            
            




    winner = ''
    if(home_sum > away_sum):
        winner = home_team
        graph.run("MATCH(c:Club {name:'"+home_team+"'})-[b:PARTICIPATES_IN]-(s:Season) set c.pointsWon = c.pointsWon + 3")
    elif(home_sum == away_sum):
        winner = "DRAW"
        graph.run("MATCH(c:Club {name:'"+home_team+"'})-[b:PARTICIPATES_IN]-(s:Season) set c.pointsWon = c.pointsWon + 1")
        graph.run("MATCH(c:Club {name:'"+away_team+"'})-[b:PARTICIPATES_IN]-(s:Season) set c.pointsWon = c.pointsWon + 1")
    else:
        winner = away_team
        graph.run("MATCH(c:Club {name:'"+away_team+"'})-[b:PARTICIPATES_IN]-(s:Season) set c.pointsWon = c.pointsWon + 3")
    graph.run("MATCH (g:Game {name:'"+sys.argv[1].split("_")[0]+" v/s "+sys.argv[1].split("_")[1]+"'}) SET g.score = '"+home_team+" "+str(home_sum)+"  -  "+str(away_sum)+" "+away_team+"', g.winner = '"+winner+"'")
    return perf_home,perf_away

def calcManOfTheMatch(home,away):
    motm = ()
    for h in home:
        if(motm == ()):
            motm = (h,home[h])
        else:
            if(motm[1]<home[h]):
                motm = (h,home[h])
    
    for h in away:
        if(motm == ()):
            motm = (h,away[h])
        else:
            if(motm[1]<away[h]):
                motm = (h,away[h])

    return motm



home_team = sys.argv[1].split("_")[0]
away_team = sys.argv[1].split("_")[1]
print(away_team)
home_players = get_list_of_players(home_team)
away_players = get_list_of_players(away_team)
print("Away players are {}".format(away_players))
calc_stats(home_team,home_players)
calc_stats(away_team,away_players)
perf_home,perf_away = findWinnerAndCalcPerf(home_team,home_players,away_team,away_players)

manOfTheMatch = calcManOfTheMatch(perf_home,perf_away)
print("Man of the match is {}".format(manOfTheMatch))
graph.run("MATCH (g {name:'"+home_team+" v/s "+away_team+"'}) set g.ManOfTheMatch = '"+manOfTheMatch[0]+"'")
for x in mycol.find({"Name":manOfTheMatch[0]},{"ManOfTheMatch":1}):
    x["ManOfTheMatch"] = int(x["ManOfTheMatch"]) + 1
    mycol.find_one_and_update({"Name":manOfTheMatch[0]},{"$set":{"ManOfTheMatch":x["ManOfTheMatch"]}})





