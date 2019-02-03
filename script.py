import subprocess
import redis
import pymongo

rd = redis.Redis("localhost")

from py2neo import Graph, Node, Relationship
graphHost='localhost'
graphUser = "neo4j"
graphPassphrase = "chinmay007"
graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FootballDBMongo"]
mycol = mydb["Milestones"]

def RemoveSpaceTeam(home):
    if " " in home:
        return home.replace(" ","_")
    return home

def subsitute(key,value,graph,home_team,away_team):
    out_player = value.split('_')[0]
    in_player = value.split('_')[2]
    graph.run("MATCH(p:Player {name:'"+out_player+"'})-[e:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.out_time = '"+key+"'")
    graph.run("MATCH(p:Player {name:'"+in_player+"'}),(g:Game {name:'"+home_team+" v/s "+away_team+"'}) MERGE (p)-[s:PLAYS {in_time:'"+key+"', out_time:0, goals:0, assists:0, yellow_cards:0, red_cards:0, passes:0, tackles:0, goals_saved:0, fouls:0, dribbles:0, shots:0, chances:0}]->(g)")
    #graph.run("MATCH(p:Player {name:'"+in_player+"'}),(g:Game {name:'"+home_team+" v/s "+away_team+"'}) MERGE (g)-[e:END {out_time:'90'}]->(p)")



def cards(key,value,graph,home_team,away_team):
    card = value.split('_')[1]
    player = value.split('_')[0]
    if(card == 'RED'):
        graph.run("MATCH(p:Player {name:'"+player+"'})-[e:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.out_time = '"+key+"',e.red_card = '1'")
        #Code to update red card count in mongo
    else:
        yellow_card = 0
        for card in graph.run("MATCH(p:Player {name:'"+player+"'})-[e:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) set e.yellow_cards = e.yellow_cards + 1 return e.yellow_cards as cards"):
            yellow_card = card["cards"]
        #player_yellow_card["cards"][0] = str(int(player_yellow_card["cards"][0]) + 1)
        #print("Player "+player)
        
        if(yellow_card == 2):
            graph.run("MATCH(p:Player {name:'"+player+"'})-[e:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.out_time = '"+key+"'")
                #graph.run("MATCH(p:Player {name:'"+player+"'})-[e:END]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.yellow_card = '2'")

def goals_assists(key,value,graph,home_team,away_team):
    # TO BE EXECUTED

    player_scored = value.split('_')[0]
    graph.run("MATCH(p:Player {name:'"+player_scored+"'})-[e:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.goals = e.goals + 1")

        

    if(len(value.split('_')) == 4):
        player_assisted = value.split('_')[2]
        graph.run("MATCH(p:Player {name:'"+player_assisted+"'})-[e:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET e.assists = e.assists + 1")


'''def set_starting_xi(key,value,graph,home_team,away_team):
    #club_name = key.split("_")[0]
    #list_of_players = []
    #for player in graph.run("MATCH(p:Player),(c:Club {name:"+club_name+"}) where exists((p)-[:BELONGS_TO]-(c)) return p.name as name"):
        #list_of_players.append(player["name"])
    players = value.split("_")
    print(players)
    for player in players:
        graph.run("MATCH(p:Player {name:'"+player+"'}),(g:Game {name:'"+home_team+" v/s "+away_team+"'}) MERGE (p)-[s:START {in_time:'00'}]->(g)")
        graph.run("MATCH(p:Player {name:'"+player+"'}),(g:Game {name:'"+home_team+" v/s "+away_team+"'}) MERGE (g)-[e:END]->(p)")'''
def convert(previous):
    for ele in previous:
          #print(type(previous[ele]))
          return (str(ele,'utf-8'),str(previous[ele],'utf-8'))
         # return str(previous[ele],'utf-8')


def check_previous_event(current,previous,x,events,home_events,away_events):
    previous_key,previous_value = convert(previous)
    
    current_key = int(str(current,'utf-8'))
    



    #previous_value = convert(current,previous)
   # print(type(previous_value))
    if("DRIBBLES" in previous_value):
        for club in graph.run("MATCH (p:Player {name:'"+previous_value.split("_")[0]+"'})-[q:BELONGS_TO]-(c:Club) return c.name as name"):
            club_name = club["name"]
        if(club_name == x.split("_")[0]):
            home_events = home_events + 1
        else:
            away_events = away_events + 1    
        events = events + 1
        
        print("CK {}".format(type(current_key)))
        print("PK {}".format(previous_key))
        diff = current_key - int(previous_key)
        print("The type of difference is {}".format(type(diff)))
        print("The difference is {}".format(diff))
        player = previous_value.split("_")[0]
        graph.run("MATCH (p:Player {name:'"+player+"'})-[r:PLAYS]-(g:Game {name:'"+x.split("_")[0]+" v/s "+x.split("_")[1]+"'}) SET r.dribbles = r.dribbles + "+str(diff)+"")
    return events,home_events,away_events


def checkMilestone(key,value,graph,home_team,away_team):
    totalGoals = 0
    for g in graph.run("MATCH (s:Season) return s.goals as goals"):
        totalGoals = totalGoals + g["goals"]
    totalGoals = totalGoals + 1
    for g in graph.run("MATCH (p:Player {name:'"+value.split("_")[0]+"'})-[q:PLAYS]-(r:Game {name:'"+home_team+" v/s "+away_team+"'}), (p:Player {name:'"+value.split("_")[0]+"'})-[b:BELONGS_TO]-(c:Club), (r:Game)-[x:PART_OF]-(s:Season) set s.goals = s.goals + 1 return c.name as name"):

        if(totalGoals % 2 == 0):
            againstTeam = ''
            print("Goal scored by {}".format(value.split("_")[0]))

            print("Playing for {}".format(g["name"]))
            if(g["name"] == home_team):
                againstTeam = away_team
                print("Against {}".format(away_team))
            else:
                againstTeam = home_team
                print("Against {}".format(home_team))
            print("At time {}".format(key))
            print("This is goal number {}".format(totalGoals))
            print("Milestone number {}".format(totalGoals // 2))
            mycol.insert_one({str(totalGoals//2):{"Goal Number":totalGoals,"Scored By":value.split("_")[0],"Playing for":g["name"],"Against":againstTeam,"Minutes":key}})




    
    
       



def game(x):
    checked_items=[]
    events,home_events,away_events = 0,0,0
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
        previous_event = {}
        #print(tmp)
        #print(b'end' in rd.hgetall(x))
        check = False
        while(True):
            if(tmp<=len(rd.hgetall(x))):
                for y in rd.hgetall(x):
                    if(y not in checked_items):
                        #print(y,rd.hgetall(x)[y])
                        if previous_event!={}:
                            events,home_events,away_events = check_previous_event(y,previous_event,x,events,home_events,away_events)
                        events,home_events,away_events = neo4j({y:rd.hgetall(x)[y]},x,events,home_events,away_events)
                        print(str(rd.hgetall(x)[y],'utf-8'))
                        if(str(rd.hgetall(x)[y],'utf-8') == "game end"):
                            print("About to brake")
                            check = True
                            break
                        previous_event = {y:rd.hgetall(x)[y]}
                        checked_items.append(y)
                if(check == True):
                    break
                tmp = len(rd.hgetall(x))
        print("Never breaked")



def end(key,value,graph,home_team,away_team):
    graph.run("MATCH (p:Player)-[r:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) WHERE r.out_time = 0 SET r.out_time = '"+key+"'")

def passed(key,value,graph,home_team,away_team):
    player = value.split("_")[0]

    graph.run("MATCH (p:Player {name:'"+player+"'})-[r:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET r.passes = r.passes + 1")

def tackled(key,value,graph,home_team,away_team):
    player = value.split("_")[0]
    
    graph.run("MATCH (p:Player {name:'"+player+"'})-[r:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET r.tackles = r.tackles + 1")

def goals_saved(key,value,graph,home_team,away_team):
    player = value.split("_")[0]
    
    graph.run("MATCH (p:Player {name:'"+player+"'})-[r:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET r.goals_saved = r.goals_saved + 1")

def fouls(key,value,graph,home_team,away_team):
    player = value.split("_")[0]
    graph.run("MATCH (p:Player {name:'"+player+"'})-[r:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET r.fouls = r.fouls + 1")
    


def chance(key,value,graph,home_team,away_team):
    player = value.split("_")[0]
    
    graph.run("MATCH (p:Player {name:'"+player+"'})-[r:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET r.chances = r.chances + 1")


def shot(key,value,graph,home_team,away_team):
    player = value.split("_")[0]
    graph.run("MATCH (p:Player {name:'"+player+"'})-[r:PLAYS]-(g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET r.shots = r.shots + 1")

def neo4j(x,game,events,home_events,away_events):
    
    home_team = game.split("_")[0]
    away_team = game.split("_")[1]


    for element in x:
        key = str(element,'utf-8')
        #print(key)
        value = str(x[element],'utf-8')
    if("OUT" in value):
        print("Substitution")
        subsitute(key,value,graph,home_team,away_team)
        print("Executed OUT")
    elif("YELLOW" in value or "RED" in value):
        print("Yellow Card")
        cards(key,value,graph,home_team,away_team)
        print("Executed CARDS")
    elif("GOAL" in value or "SCORES" in value):
        checkMilestone(key,value,graph,home_team,away_team)
        print("Goal Scored")
        for club in graph.run("MATCH (p:Player {name:'"+value.split("_")[0]+"'})-[q:BELONGS_TO]-(c:Club) return c.name as name"):
            club_name = club["name"]
        if(club_name == home_team):
            home_events = home_events + 1
        else:
            away_events = away_events + 1    
        events = events + 1
        goals_assists(key,value,graph,home_team,away_team)
        print("Executed GOALS")
    elif("PASSED" in value):
        for club in graph.run("MATCH (p:Player {name:'"+value.split("_")[0]+"'})-[q:BELONGS_TO]-(c:Club) return c.name as name"):
            club_name = club["name"]
        if(club_name == home_team):
            home_events = home_events + 1
        else:
            away_events = away_events + 1    
        events = events + 1
        passed(key,value,graph,home_team,away_team)
        print("Executed PASSED")
    elif("TACKLED" in value or "INTERCEPTED" in value or "BLOCKED" in value):
        for club in graph.run("MATCH (p:Player {name:'"+value.split("_")[0]+"'})-[q:BELONGS_TO]-(c:Club) return c.name as name"):
            club_name = club["name"]
        if(club_name == home_team):
            home_events = home_events + 1
        else:
            away_events = away_events + 1    
        events = events + 1
        tackled(key,value,graph,home_team,away_team)
        print("Executed TACKLED")
    elif("GOAL_SAVED" in value or "SAVED" in value):
        for club in graph.run("MATCH (p:Player {name:'"+value.split("_")[0]+"'})-[q:BELONGS_TO]-(c:Club) return c.name as name"):
            club_name = club["name"]
        if(club_name == home_team):
            home_events = home_events + 1
        else:
            away_events = away_events + 1    
        events = events + 1
        goals_saved(key,value,graph,home_team,away_team)
        print("Executed GOALS_SAVED")
    elif("FOUL" in value):
        fouls(key,value,graph,home_team,away_team)
        print("Executed Fouls")
    elif("CORNER" in value):
        for club in graph.run("MATCH (p:Player {name:'"+value.split("_")[0]+"'})-[q:BELONGS_TO]-(c:Club) return c.name as name"):
            club_name = club["name"]
        if(club_name == home_team):
            home_events = home_events + 1
        else:
            away_events = away_events + 1    
        events = events + 1
        for club in graph.run("MATCH (p:Player {name:'"+value.split('_')[0]+"'})-[s:BELONGS_TO]->(c:Club),(p:Player {name:'"+value.split('_')[0]+"'})-[q:PLAYS]->(r:Game {name:'"+home_team+" v/s "+away_team+"'}) return c.name as name"):
            club_name = club["name"]
        if(" " in club_name):
            club_name = club_name.replace(" ","_")
        graph.run("MATCH (g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET g."+club_name+"_corners = g."+club_name+"_corners + 1")
        print("Executed Corners")
    elif("OFFSIDE" in value):
        print("Outside the offside loop")
        for club in graph.run("MATCH (p:Player {name:'"+value.split('_')[0]+"'})-[s:BELONGS_TO]->(c:Club),(p:Player {name:'"+value.split('_')[0]+"'})-[q:PLAYS]->(r:Game {name:'"+home_team+" v/s "+away_team+"'}) return c.name as name"):
            club_name = club["name"]
        if(" " in club_name):
            club_name = club_name.replace(" ","_")
        graph.run("MATCH (g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET g."+club_name+"_offsides = g."+club_name+"_offsides + 1")
        print("Executed Foulss")
    elif("end" in value):
        print("Game Ended")
        print(home_events,away_events,events)
        end(key,value,graph,home_team,away_team)
        graph.run("MATCH (g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET g."+RemoveSpaceTeam(home_team)+"_possession = "+str((home_events/events))+" * 100")
        graph.run("MATCH (g:Game {name:'"+home_team+" v/s "+away_team+"'}) SET g."+RemoveSpaceTeam(away_team)+"_possession = "+str((away_events/events))+" * 100")
        print("Executed GAME ENDED")
    elif("CHANCE" in value or "CROSSED" in value):
        for club in graph.run("MATCH (p:Player {name:'"+value.split("_")[0]+"'})-[q:BELONGS_TO]-(c:Club) return c.name as name"):
            club_name = club["name"]
        if(club_name == home_team):
            home_events = home_events + 1
        else:
            away_events = away_events + 1    
        events = events + 1
        chance(key,value,graph,home_team,away_team)
        print("Executed Chances")
    elif("SHOOTS" in value):
        for club in graph.run("MATCH (p:Player {name:'"+value.split("_")[0]+"'})-[q:BELONGS_TO]-(c:Club) return c.name as name"):
            club_name = club["name"]
        if(club_name == home_team):
            home_events = home_events + 1
        else:
            away_events = away_events + 1    
        events = events + 1
        shot(key,value,graph,home_team,away_team)
        print("Executed Shots")
    else:
        print("Game ontinue")
    return events,home_events,away_events

game("Manchester United_Arsenal")
print("Now executing next script")
subprocess.run(["python","match_stats.py","Manchester United_Arsenal"])




