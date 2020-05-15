from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

def scrap(url):
    #This is fuction for scrapping
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    #Find the key to get the information
    table = soup.find('table', attrs={'class':'table'}) 
    tr = table.find_all('tr') 

    temp = [] #initiating a tuple

    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]
         
        #get tanggal 
        Tanggal = row.find_all('td')[0].text
        Tanggal =  Tanggal.strip() #for removing the excess whitespace
        
        #get inflasi
        Kurs_Jual = row.find_all('td')[1].text
        Kurs_Jual = Kurs_Jual.strip() #for removing the excess whitespace

        #get inflasi
        Kurs_Beli = row.find_all('td')[2].text
        Kurs_Beli = Kurs_Beli.strip() #for removing the excess whitespace
        
        temp.append((Tanggal,Kurs_Jual,Kurs_Beli)) 
        
    temp = temp[::-1] #remove the header

    df = pd.DataFrame(temp, columns = ('Tanggal','Kurs_Jual','Kurs_Beli')) #creating the dataframe
   #data wranggling -  try to change the data type to right data type
    df['Tanggal']=df['Tanggal'].str.replace("Mei","May")
    df['Tanggal']=df['Tanggal'].str.replace("Januari","Jan")
    df['Tanggal']=df['Tanggal'].str.replace("Februari","Feb")
    df['Tanggal']=df['Tanggal'].str.replace("Maret","Mar")
    df['Tanggal']=df['Tanggal'].str.replace("April","Apr")
    df['Tanggal']=df['Tanggal'].str.replace("Juni","Jun")
    df['Tanggal']=df['Tanggal'].str.replace("Juli","Jul")
    df['Tanggal']=df['Tanggal'].str.replace("Agustus","Aug")
    df['Tanggal']=df['Tanggal'].str.replace("September","Sep")
    df['Tanggal']=df['Tanggal'].str.replace("Oktober","Oct")
    df['Tanggal']=df['Tanggal'].str.replace("November","Nov")
    df['Tanggal']=df['Tanggal'].str.replace("Desember","Dec")
    df['Kurs_Jual'] = df['Kurs_Jual'].str.replace(",",".")
    df['Kurs_Beli'] = df['Kurs_Beli'].str.replace(",",".")
    df['Kurs_Jual']=df['Kurs_Jual'].astype('float')
    df['Kurs_Beli']=df['Kurs_Beli'].astype('float')
    df['Tanggal']=df['Tanggal'].astype('datetime64')
    df = df.sort_values(by='Tanggal').set_index('Tanggal')
    

   #end of data wranggling

    return df

@app.route("/")
def index():
    df = scrap('https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=30-12-2019') #insert url here

    #This part for rendering matplotlib
    fig = plt.figure(figsize=(5,2),dpi=300)
    df.plot()
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df, result=result)


if __name__ == "__main__": 
    app.run()
