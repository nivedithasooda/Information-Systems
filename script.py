import redis
from py2neo import Graph, Node, Relationship

rd = redis.Redis("localhost")

def subsitute(key,value,graph,home_team,away_team):
    out_player = value.split('_')[1]
    in_player = value.split('_')[3]
    graph.run("MATCH(p:Player {name:'"+out_player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.end_time = '"+key+"'")
    graph.run("MATCH(p:Player {name:'"+in_player+"'}),(g:Game {name:'"+home_team+" v/s "+away_team+"'}) MERGE (p)-[s:START {start_time:'"+key+"'}]->(g)")
    graph.run("MATCH(p:Player {name:'"+in_player+"'}),(g:Game {name:'"+home_team+" v/s "+away_team+"'}) MERGE (g)-[e:END {end_time:'90'}]->(p)")



def cards(key,value,graph,home_team,away_team):
    card = value.split('_')[0]
    player = value.split('_')[1]
    if(card == 'RED'):
        graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.end_time = '"+key+"',e.red_card = '1'")
        #Code to update red card count in mongo
    else:
        player_yellow_card = graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) return e as cards")
        if('yellow_cards' in player_yellow_card["cards"]):
            player_yellow_card["cards"].yellow_card = str(int(player_yellow_card["cards"].yellow_card) + 1)
            if(player_yellow_card["cards"].yellow_card == 2):
                graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.end_time = '"+key+"',e.yellow_card = '2'")
                #graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.yellow_card = '2'")
            else:
                graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.end_time = '"+player_yellow_card["cards"].yellow_card+"'")
        else:
            graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.yellow_card = '1'")


def goals_assists(key,value,graph,home_team,away_team):
    # TO BE EXECUTED
    if(len(value.split('_')) == 2):
        player = value.split('_')[1]
        player_yellow_card = graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) return n as cards")
        graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.end_time = '"+key+"',e.yellow_card = '2'")
    
    else:


    



def set_starting_xi(key,value,graph,home_team,away_team):
    #club_name = key.split("_")[0]
    #list_of_players = []
    #for player in graph.run("MATCH(p:Player),(c:Club {name:"+club_name+"}) where exists((p)-[:BELONGS_TO]-(c)) return p.name as name"):
        #list_of_players.append(player["name"])
    players = value.split("_")
    print(players)
    for player in players:
        graph.run("MATCH(p:Player {name:'"+player+"'}),(g:Game {name:'"+home_team+" v/s "+away_team+"'}) MERGE (p)-[s:START {start_time:'00'}]->(g)")
        graph.run("MATCH(p:Player {name:'"+player+"'}),(g:Game {name:'"+home_team+" v/s "+away_team+"'}) MERGE (g)-[e:END]->(p)")

def game(x):
    checked_items=[]
    print(str(rd.keys()[0], 'utf-8'))
    flag = False
    print(str(rd.keys()[0], 'utf-8') == x)
    for a in rd.keys():
        if(str(a,'utf-8') == x):
            flag = True
            break
    if flag == True:
        print("Game found {}".format(x))
        tmp = len(rd.hgetall(x))
        #print(tmp)
        #print(b'end' in rd.hgetall(x))
        while(not b'end' in rd.hgetall(x)):
            if(tmp<=len(rd.hgetall(x))):
                for y in rd.hgetall(x):
                    if(y not in checked_items):
                        #print(y,rd.hgetall(x)[y])
                        neo4j({y:rd.hgetall(x)[y]},x)
                        checked_items.append(y)
                tmp = len(rd.hgetall(x))
        print(rd.hgetall(x)[b'end'])
        #neo4j({b'end':rd.hgetall(x)[b'end']})


def neo4j(x,game):
    graphHost='localhost'
    graphUser = "neo4j"
    graphPassphrase = "chinmay007"
    graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)
    home_team = game.split("_")[0]
    away_team = game.split("_")[1]


    for element in x:
        key = str(element,'utf-8')
        print(key)
        value = str(x[element],'utf-8')
    if("OUT" in value):
        print("Substitution")
        subsitute(key,value,graph,home_team,away_team)
    elif("YELLOW" in value or "RED" in value):
        print("Yellow Card")
        cards(key,value,graph,home_team,away_team)
    elif("Starting XI" in key):
        set_starting_xi(key,value,graph,home_team,away_team)
        print("Set edges")
    elif("GOAL" in value):
        print("Goal Scored")
        goals_assists(key,value,graph,home_team,away_team)
    else:
        print("Game Ended")





game("Manchester United_Arsenal")







    
