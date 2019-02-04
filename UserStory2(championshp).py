import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["FootballDBMongo"]

#titles won by the club
print("To view seasons in which the club won EPL championship")
userInputClub = input("     Enter the name of the club  : ")

championshipQuery1 = {"$and":[{"name":userInputClub},{"TitlesWon.TrophyName" : "EPL"}]}
championshipQuery2 = {"TitlesWon":1, "_id":0}

databaseCollection = mydb.clubStats.find_one(championshipQuery1,championshipQuery2)

if(databaseCollection == 0):
    print("              No championship found")
    
else:
    
    for titles in databaseCollection:
        print("      Year in which the club won EPL Championship")
        print("           Year                Title")
        for w in databaseCollection[titles]:
            if(w["TrophyName"] == "EPL"):
                print("           {}                {}".format(w["year"],w["TrophyName"]))
        print()
        x = w["year"]
        for w in databaseCollection[titles]:
            if(w["year"] != x ):
            #if(w1["Year"] == w["year"]):
                        seasonQuery1 = {"$and":[{"name": userInputClub},{"SeasonPoints.Points":{"$gt": "18"}}]}
                        seasonQuery2 = {"SeasonPoints.$":1 ,"_id" :0}
                        databaseCollection1 = mydb.clubStats.find_one(seasonQuery1,seasonQuery2)
                        
                        for season in databaseCollection1:
                            print("      Points earned in the season ")
                            print("           Year                PointsEarned")
                            for w1 in databaseCollection1[season]:
                                if(w1["Year"] == w["year"]):
                                    print("           {}                {}".format(w1["Year"],w1["Points"]))
                            print()
      


            