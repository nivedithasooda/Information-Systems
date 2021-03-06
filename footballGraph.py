import redis
from py2neo import Graph, Node, Relationship

def createSeasons(label,season,graph):#season
        graph.run("CREATE (n:"+label+" {name:'Year"+season+"'})")

#CREATE SEASON FIRST and then execute
def createClubNodeAndrelations(label,club,year,season,graph):#club
    graph.run("CREATE (n:"+label+" {name:'"+club+"', year: '"+year+"'})")
    graph.run("MATCH(p:"+label+" {name:'"+club+"', year: '"+year+"'}), (g:Season {name:'"+season+"'}) MERGE (p)-[s:PARTICIPATED_IN]->(g)")
  

#CREATE CLUBS AND SEASONS FIRST and then execute
def createGameNodeAndrelations(label,game,club,opponent,year,season,graph):#game
    graph.run("CREATE (n:"+label+" {name:'"+game+"', "+club+"_fouls: 0, "+club+"_offsides: 0, "+club+"_corners: 0, "+club+"_totalShots: 0, "+club+"_yellowCards: 0, "+club+"_redCards: 0, "+club+"_possession: 0, "+opponent+"_fouls: 0, "+opponent+"_offsides: 0, "+opponent+"_corners: 0, "+opponent+"_totalShots: 0, "+opponent+"_yellowCards: 0, "+opponent+"_redCards: 0, "+opponent+"_possession: 0})")
    graph.run("MATCH(p:"+label+" {name:'"+game+"'}), (g:Season {name:'"+season+"'}) MERGE (p)<-[s:GAME_PLAYED]-(g)")
    
#create clubs and games first and then execute
def createPlayerNodeAndrelations(label,player,club,games,year,graph):#players
    graph.run("CREATE (n:"+label+" {name:'"+player+"', year:'"+year+"'}) return n")
    graph.run("MATCH(p:"+label+" {name:'"+player+"', year:'"+year+"'}), (g:Club {name:'"+club+"', year:'"+year+"'}) MERGE (p)-[s:BELONGS_TO]->(g)")
    for game in games:
        graph.run("MATCH(p:"+label+" {name:'"+player+"', year:'"+year+"'}), (g:Game {name:'"+game+"'}) MERGE (p)-[s:PLAYS]->(g)")
        graph.run("MATCH(p:"+label+" {name:'"+player+"', year:'"+year+"'})-[r:PLAYS]-(g:Game {name:'"+game+"'}) SET r.goals = 0, r.assists = 0, r.yellow_cards = 0, r.red_cards = 0, r.passes = 0, r.tackles = 0, r.goals_saved = 0, r.in_time = 0, r.out_time = 0, r.fouls = 0, r.dribbles = 0")
        
def neo4j():
    graphHost='localhost'
    graphUser = "neo4j"
    graphPassphrase = "01test"
    graph=Graph(bolt=True, host=graphHost, user=graphUser, password=graphPassphrase)
    years=["2017","2018"]# provide season/years

    #create seasons and club relationships
    for year in years:
        createSeasons("Season",year,graph)
        season="Year"+year
        clubs=["Manchester United","Chelsea","Arsenal","Liverpool"]# provide club names
        for club in clubs:
            if((year == "2017" and club=="Arsenal") or (year=="2018" and club=="Liverpool")):
                continue
            createClubNodeAndrelations("Club",club,year,season,graph)
        
        #after successful creation of season, clubs and relationships
        for club in clubs:
            clubName=club.replace(' ','_')
            if((year == "2018" and club=="Arsenal") or (year=="2017" and club=="Liverpool")):
                createGameNodeAndrelations("Game",club+" v/s Manchester United "+year,club,"Manchester_United",year,season,graph)
                createGameNodeAndrelations("Game",club+" v/s Chelsea "+year,club,"Chelsea",year,season,graph)
            elif(club=="Chelsea"):
                createGameNodeAndrelations("Game",club+" v/s Manchester United "+year,club,"Manchester_United",year,season,graph)                
                if(year == "2017"):
                    createGameNodeAndrelations("Game",club+" v/s Liverpool "+year,club,"Liverpool",year,season,graph)
                elif(year=="2018"):
                    createGameNodeAndrelations("Game",club+" v/s Arsenal "+year,club,"Arsenal",year,season,graph)
            elif(club=="Manchester United"):
                createGameNodeAndrelations("Game",club+" v/s Chelsea "+year,clubName,"Chelsea",year,season,graph)
                if(year == "2017"):
                    createGameNodeAndrelations("Game",club+" v/s Liverpool "+year,clubName,"Liverpool",year,season,graph)
                elif(year=="2018"):
                    createGameNodeAndrelations("Game",club+" v/s Arsenal "+year,clubName,"Arsenal",year,season,graph)

        #after creation of games and relationships  
        # add all players for each season and mention matches they played for  
        for club in clubs:
            if((year=="2017" and club=="Arsenal")or(year=="2018" and club=="Liverpool")):
                continue
            else:
                if(year=="2017"):
                    if(club=="Manchester United"):
                        #players playing 
                        createPlayerNodeAndrelations("Player:Keeper","Sergio Romero",club,[club+" v/s Chelsea "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Eric Bailly",club,[club+" v/s Chelsea "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Andreas Pereira",club,[club+" v/s Chelsea "+year, "Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Anthony Martial",club,[club+" v/s Chelsea "+year,"Chelsea v/s "+club+" " +year,"Liverpool v/s "+club+" " +year],year,graph)
                        createPlayerNodeAndrelations("Player","Luke Shaw",club,[club+" v/s Liverpool "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" " +year,"Liverpool v/s " +club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Diogo Dalot",club,[club+" v/s Liverpool "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" " +year,"Liverpool v/s "+club+" " +year],year,graph)
                        createPlayerNodeAndrelations("Player","Ashley Young",club,[club+" v/s Liverpool "+year,club+" v/s Chelsea "+year, "Chelsea v/s " +club+ " "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Paul Pogba",club,[club+" v/s Liverpool "+year,club+" v/s Chelsea "+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Juan Mata",club,[club+" v/s Liverpool "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" " +year,"Liverpool v/s "+club+" " +year],year,graph)
                        createPlayerNodeAndrelations("Player","Marcus Rashford",club,[club+" v/s Liverpool "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" " +year,"Liverpool v/s "+club+" " +year],year,graph)
                        createPlayerNodeAndrelations("Player","Jesse Lingard",club,[club+" v/s Liverpool "+year,club+" v/s Chelsea "+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","Lee Grant",club,[club+" v/s Liverpool "+year,"Chelsea v/s "+club+" "+year ,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Antonio Valencia",club,[club+" v/s Liverpool "+year,"Chelsea v/s "+club+" " +year,"Liverpool v/s "+club+" " +year],year,graph)
                        createPlayerNodeAndrelations("Player","Nemanja Matic",club,[club+" v/s Liverpool "+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Romelu Lukaku",club,[club+" v/s Liverpool "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Scott McTominay",club,["Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Victor Lindelof",club,["Liverpool v/s "+club+" "+year],year,graph)

                        
                        #players playing nowhere
                        createPlayerNodeAndrelations("Player","Ander Herrera",club,[],year,graph)
                        createPlayerNodeAndrelations("Player","Marouane Fellaini",club,[],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","David de Gea",club,[],year,graph)

                    elif(club=="Chelsea"):
                        #players playing 
                        createPlayerNodeAndrelations("Player:Keeper","Kepa",club,[club+" v/s Liverpool "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Robert Green",club,["Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Davide Zappacosta",club,[club+" v/s Liverpool "+year,"Manchester United v/s "+club+" "+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Cesar Azpilicueta",club,[club+" v/s Liverpool "+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Jorginho",club,[club+" v/s Liverpool "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Mateo Kovacic",club,[club+" v/s Liverpool "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Olivier Giroud",club,[club+" v/s Liverpool "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Andreas Christensen",club,[club+" v/s Liverpool "+year,club+" v/s Manchester United"+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Marcos Alonso",club,[club+" v/s Liverpool "+year,club+" v/s Manchester United"+year,"Manchester United v/s "+club+" "+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Ross Barkley",club,[club+" v/s Liverpool "+year,club+" v/s Manchester United"+year,"Liverpool v/s "+club+" "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Eden Hazard",club,[club+" v/s Liverpool "+year,club+" v/s Manchester United"+year,"Manchester United v/s "+club+" "+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Pedro",club,[club+" v/s Liverpool "+year,club+" v/s Manchester United "+year,"Manchester United v/s "+club+" "+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","Willy Caballero",club,[club+" v/s Manchester United"+year],year,graph)
                        createPlayerNodeAndrelations("Player","Antonio Rudiger",club,[club+" v/s Manchester United"+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Emerson",club,[club+" v/s Manchester United"+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Ruben Loftus Cheek",club,[club+" v/s Manchester United"+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Danny Drinkwater",club,[club+" v/s Manchester United"+year],year,graph)
                        createPlayerNodeAndrelations("Player","Gonzalo Higuain",club,[club+" v/s Manchester United"+year,"Liverpool v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Marco van Ginkel",club,["Liverpool v/s "+club+" "+year],year,graph)

                        #no game played by
                        createPlayerNodeAndrelations("Player","N Golo Kante",club,[],year,graph)

                    elif(club=="Liverpool"):
                        #players playing 
                        createPlayerNodeAndrelations("Player:Keeper","Simon Mignolet",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Connor Randall",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Dejan Lovren",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Georginio Wijnaldum",club,[club+" v/s Chelsea "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Mohamed Salah",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Andrew Robertson",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Trent Alexander Arnold",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","James Milner",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Alex Oxlade Chamberlain",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Divock Origi",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Sadio Mane",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Virgil van Dijk",club,[club+" v/s Manchester United "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Joe Gomez",club,[club+" v/s Manchester United "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","Alisson",club,[club+" v/s Manchester United "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Adam Lallana",club,[club+" v/s Manchester United "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Daniel Sturridge",club,[club+" v/s Manchester United "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Fabinho",club,["Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        #no game played by players
                        createPlayerNodeAndrelations("Player","Jordan Henderson",club,[],year,graph)
                        createPlayerNodeAndrelations("Player","Caoimhin Kelleher",club,[],year,graph)
                        createPlayerNodeAndrelations("Player","Naby Keita",club,[],year,graph)
                elif(year=="2018"):                
                    if(club=="Arsenal"):
                        #players playing 
                        createPlayerNodeAndrelations("Player:Keeper","Bernd Leno",club,[club+" v/s Manchester United "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Shkodran Mustafi",club,[club+" v/s Manchester United "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Sokratis",club,[club+" v/s Manchester United "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Stephan Lichtsteiner",club,[club+" v/s Manchester United "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Granit Xhaka",club,[club+" v/s Manchester United "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Pierre Emerick Aubameyang",club,[club+" v/s Manchester United "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Mesut Ozil",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Aaron Ramsey",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Alex Iwobi",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Danny Welbeck",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Sead Kolasinac",club,[club+" v/s Manchester United "+year,club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","Petr Cech",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Hector Bellerin",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Carl Jenkinson",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Nacho Monreal",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Henrikh Mkhitaryan",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Alexandre Lacazette",club,[club+" v/s Chelsea "+year,"Manchester United v/s "+club+" "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Lucas Torreira",club,["Chelsea v/s "+club+" "+year],year,graph)
                        #no game played by players
                        createPlayerNodeAndrelations("Player","Matteo Guendouzi",club,[],year,graph)
                        createPlayerNodeAndrelations("Player","Joe Willock",club,[],year,graph)
                    elif(club=="Manchester United"):
                        #players playing 
                        createPlayerNodeAndrelations("Player","Victor Lindelof",club,[club+" v/s Chelsea"+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Antonio Valencia",club,[club+" v/s Chelsea"+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Nemanja Matic",club,[club+" v/s Chelsea"+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Paul Pogba",club,[club+" v/s Chelsea"+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Romelu Lukaku",club,[club+" v/s Chelsea"+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","David de Gea",club,[club+" v/s Arsenal "+year,club+" v/s Chelsea "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Eric Bailly",club,[club+" v/s Arsenal "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Diogo Dalot",club,[club+" v/s Arsenal "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Juan Mata",club,[club+" v/s Arsenal "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Anthony Martial",club,[club+" v/s Arsenal "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Jesse Lingard",club,[club+" v/s Arsenal "+year,club+" v/s Chelsea "+year,"Chelsea v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Luke Shaw",club,[club+" v/s Arsenal"+year,"Chelsea v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Ashley Young",club,[club+" v/s Arsenal"+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Andreas Pereira",club,[club+" v/s Arsenal"+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Scott McTominay",club,[club+" v/s Arsenal"+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Marcus Rashford",club,[club+" v/s Arsenal"+year,"Chelsea v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","Lee Grant",club,["Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","Sergio Romero",club,["Chelsea v/s "+club+" "+year],year,graph)
                        #players playing nowhere
                        createPlayerNodeAndrelations("Player","Ander Herrera",club,[],year,graph)
                        createPlayerNodeAndrelations("Player","Marouane Fellaini",club,[],year,graph)
                    elif(club=="Chelsea"):
                        #players playing 
                        createPlayerNodeAndrelations("Player","Cesar Azpilicueta",club,[club+" v/s Arsenal"+year,"Manchester United v/s "+club+" "+year,],year,graph)
                        createPlayerNodeAndrelations("Player","Emerson",club,[club+" v/s Arsenal"+year,"Manchester United v/s "+club+" "+year,],year,graph)
                        createPlayerNodeAndrelations("Player","Ruben Loftus Cheek",club,[club+" v/s Arsenal"+year,"Manchester United v/s "+club+" "+year,],year,graph)
                        createPlayerNodeAndrelations("Player","Danny Drinkwater",club,[club+" v/s Arsenal"+year],year,graph)
                        createPlayerNodeAndrelations("Player","Gonzalo Higuain",club,[club+" v/s Arsenal"+year,"Manchester United v/s "+club+" "+year,],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","Kepa",club,[club+" v/s Arsenal "+year,club+" v/s Manchester United "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Marcos Alonso",club,[club+" v/s Arsenal "+year,club+" v/s Manchester United "+year,"Manchester United v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Ross Barkley",club,[club+" v/s Arsenal "+year,club+" v/s Manchester United "+year,"Manchester United v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Davide Zappacosta",club,[club+" v/s Arsenal"+year,club+" v/s Manchester United "+year,"Manchester United v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Eden Hazard",club,[club+" v/s Arsenal "+year,club+" v/s Manchester United "+year,"Manchester United v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Pedro",club,[club+" v/s Arsenal "+year,club+" v/s Manchester United "+year,"Manchester United v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Antonio Rudiger",club,[club+" v/s Manchester United "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Andreas Christensen",club,[club+" v/s Manchester United "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Jorginho",club,[club+" v/s Manchester United "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Mateo Kovacic",club,[club+" v/s Manchester United "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Olivier Giroud",club,[club+" v/s Manchester United "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player:Keeper","Robert Green",club,["Manchester United v/s "+club+" "+year,"Arsenal v/s "+club+" "+year],year,graph)
                        createPlayerNodeAndrelations("Player","Marco van Ginkel",club,["Manchester United v/s "+club+" "+year],year,graph)
                        #no game played by
                        createPlayerNodeAndrelations("Player","N Golo Kante",club,[],year,graph)  
                        createPlayerNodeAndrelations("Player","Willy Caballero",club,[],year,graph) 
    #create relation between the 2 seasons
    graph.run("MATCH(p:Season {name:'Year2017'}), (g:Season {name:'Year2018'}) MERGE (p)-[s:NEXT]->(g)")    
neo4j()