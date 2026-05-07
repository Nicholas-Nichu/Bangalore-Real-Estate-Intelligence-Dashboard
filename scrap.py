import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=1,4,5,%3E5,2,3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Bangalore',
    'sec-ch-ua': '"Chromium";v="147", "Not.A/Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
}
Data=[]
page=1
while True:
    url=(f'https://www.magicbricks.com/mbsrp/propertySearch.html?editSearch=Y&category=S&propertyType=10002,10003,10021,10022&bedrooms=11700,11703,11704,11705,11706,11707,11708,11709,11710,11701,11702&city=3327&page={page}&sortBy=premiumRecent&postedSince=-1&pType=10002,10003,10021,10022&isNRI=N&multiLang=en')
    response = requests.get(url,headers=headers).json()
    Macro_date=response.get('resultList',[])
    if not Macro_date or page==500:
        break

    for prop in Macro_date:
        item = {
            "id": prop.get("id"),
            "title": prop.get("propertyTitle"),
            "project_name": prop.get("plgdtldesc", "").split(" in ")[0],
            "location": prop.get("lmtDName"),
            "city": prop.get("ctName"),
            "bhk": prop.get("bedroomD"),
            "price": prop.get("price"),
            "price_display": prop.get("priceD"),
            "SBA": prop.get("caSqFt"),
            "carpet_area": prop.get("carpetArea"),
            "facing": prop.get("facingD"),
            "furnishing": prop.get("furnishedD"),
            "status": prop.get("possStatusD"),
            "possession": prop.get("availableFrom"),
            "builder": prop.get("companyname"),
            "floor": prop.get("floorD"),
            "bathrooms": prop.get("bathD"),
            "balconies": prop.get("balconiesD"),
            "parking": prop.get("parkingD"),
            "amenities": prop.get("luxAmenitiesD"),
            "image": prop.get("image"),
            "url": "https://www.magicbricks.com/" + prop.get("seoURL", ""),
            "rate/Sq.ft":prop.get("sqFtPrice"),
            "launch_date":prop.get("postDateT")
        }
        Data.append(item)
    page+=1
import pandas as pd
df=pd.DataFrame(Data)
df["launch_date"]=pd.to_datetime(df["launch_date"])
df["possession"]=pd.to_datetime(df["possession"],format="%b '%y")
df.info()
from sqlalchemy import create_engine, case

engine = create_engine(
    "postgresql://postgres:password@localhost:5432/real_estate"
)
df.rename(columns={"rate/Sq.ft": "rate_per_sqft"}, inplace=True)
import numpy as np
df["SBA"]=df["SBA"].round().astype("Int64")
df["SBA"]=np.floor(df["SBA"])
df.to_sql("real_estate",engine,if_exists="append")

from bs4 import BeautifulSoup
url=requests.get('https://www.bankbazaar.com/pin-code/karnataka/bangalore.html').text
soup=BeautifulSoup(url,'xml')
x=soup.find_all('td',class_='align-middle [&:has([role=checkbox])]:pr-0 border-l p-2')
yo=[]
for i in x:
    yo.append(i.text)
yo2= []
for i in range(0,len(yo),4):
    yo2.append({"Place":yo[i],"Pincode":yo[i+1]})
yo3=pd.DataFrame(yo2)
yo3.to_sql("pincode",eng,if_exists="append")

