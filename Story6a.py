import matplotlib.pyplot as plt
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FootballDBMongo"]
mycol = mydb["clubStats"]

def calcAnnualRevenueGrowth(revenue,year):
    start = revenue[0]
    end = revenue[len(revenue)-1]
    yearRange = int(abs(year[0]-year[len(year)-1]))

    annualGrowth = (pow(end/start,1/yearRange) - 1) * 100
    print("The revenue growth for the club between 2013 to 2018 is {:.2f}%".format(annualGrowth))



club = input("Please enter the name of the club whose revenue trend you want to see ")
year = []
revenue = []


clubData = mycol.find_one({"name":club})

    
if (mycol.count_documents({"name":club}) != 0):
    for x in clubData:
    
        if(x == "AnnualRevenue"):
        
            for y in clubData[x]:
                year.append(int(y["Year"]))
                revenue.append(int(y["Revenue"]))

    calcAnnualRevenueGrowth(revenue,year)
    plt.plot(year,revenue)
    plt.xlabel('Year')
    plt.ylabel('Revenue in millions of Euros')
    plt.show()

else:
    print("Sorry! not able to find the club")

#References : 
#Calculation of annual revenue growth % : https://www.fool.com/knowledge-center/how-to-calculate-revenue-growth-for-3-years.aspx
#Revenues of football clubs in million euros : https://en.wikipedia.org/wiki/Deloitte_Football_Money_League#2018

