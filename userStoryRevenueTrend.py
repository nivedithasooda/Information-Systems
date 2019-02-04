import matplotlib.pyplot as plt
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FootballDBMongo"]
mycol = mydb["clubStats"]

club = input("Please enter the name of the club whose revenue trend you want to see")
year = []
revenue = []
clubData = mycol.find_one({"name":club})
print(clubData["name"])
for x in clubData:
    
    if(x == "AnnualRevenue"):
        print("FOUND")
        for y in clubData[x]:
            year.append(int(y["Year"]))
            revenue.append(int(y["Revenue"]))
plt.plot(year,revenue)
plt.show()





