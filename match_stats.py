import sys
from py2neo import Graph, Node, Relationship
graphHost='localhost'
graphUser = "neo4j"
graphPassphrase = "chinmay007"
graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)

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
        for g in graph.run("MATCH (p:Player {name:'"+p+"'})-[q:PLAYS]-(g:Game {name:'"+sys.argv[1].split("_")[0]+" v/s "+sys.argv[1].split("_")[1]+"'}) return q.goals as goals, q.assists as assists, q.chances as chances, q.tackles as tackles, q.passes as passes, q.goals_saved as goals_saved"):
            home_sum = home_sum + g["goals"]
            player_score = (1 * g["goals"]) + (0.75 * g["assists"]) + (0.65 * g["chances"]) + (0.5 * g["tackles"]) + (0.25 * g["passes"]) + (0.75 * g["goals_saved"])
            perf_home[p] = player_score 

    for p in away_players:
        player_score = 0
        for g in graph.run("MATCH (p:Player {name:'"+p+"'})-[q:PLAYS]-(g:Game {name:'"+sys.argv[1].split("_")[0]+" v/s "+sys.argv[1].split("_")[1]+"'}) return q.goals as goals, q.assists as assists, q.chances as chances, q.tackles as tackles, q.passes as passes, q.goals_saved as goals_saved"):
            away_sum = away_sum + g["goals"]
            player_score = (1 * g["goals"]) + (0.75 * g["assists"]) + (0.65 * g["chances"]) + (0.5 * g["tackles"]) + (0.25 * g["passes"]) + (0.75 * g["goals_saved"])
            perf_away[p] = player_score
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


home_team = sys.argv[1].split("_")[0]
away_team = sys.argv[1].split("_")[1]
print(away_team)
home_players = get_list_of_players(home_team)
away_players = get_list_of_players(away_team)
print("Away players are {}".format(away_players))
calc_stats(home_team,home_players)
calc_stats(away_team,away_players)
perf_home,perf_away = findWinnerAndCalcPerf(home_team,home_players,away_team,away_players)

for a in perf_home:
    print("The name of the player is {} and his performance is {}".format(a,perf_home[a]))

for a in perf_away:
    print("The name of the player is {} and his performance is {}".format(a,perf_away[a]))



