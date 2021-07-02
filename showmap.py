import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from bs4 import BeautifulSoup
import requests
import re
import random
import urllib
def data_bulanan():
    #Load and Processing Data
    last_update=requests.get('https://covid19.who.int/')
    last_update = BeautifulSoup(last_update.content,'html.parser')
    last_up=last_update.find_all('h2')[1].find_all('span')[1].text
    # last_up=last.split(': ')[1].split(',')
    # last_up=' '.join(last_up)
    with open('bulanan_last','r') as baca:
        data_offline=baca.read()
    if last_up==data_offline :
        data=pd.read_csv('offline_bulanan.csv')
        data['Date_reported']=data['Date_reported'].apply(pd.to_datetime)
        data[['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']] = data[['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']].apply(pd.to_numeric)
        data.set_index('Date_reported',inplace=True)
        # data.drop('Unnamed 1:',axis =1,inplace=True)
        nat_group=data.groupby('Country')
    else:
        urllib.request.urlretrieve('https://covid19.who.int/WHO-COVID-19-global-data.csv','offline_bulanan.csv')
        # list_data=str(data.content).split('\\n')
        # list_data.remove(list_data[0])
        # list_data.remove(list_data[-1])
        # for i in range(len(list_data)):
        #     if len(list_data[i].split(','))==9:
        #         wew=list_data[i].split('"')
        #         wew=wew[0].split(',')+[wew[1]]+wew[2].split(',')
        #         wew.remove('')
        #         wew.remove('')
        #         list_data[i]=wew
        #     else:
        #         list_data[i]=list_data[i].split(',')
        data_covid=pd.read_csv('offline_bulanan.csv')
        data_covid['Date_reported']=data_covid['Date_reported'].apply(pd.to_datetime)
        data_covid[['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']] = data_covid[['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']].apply(pd.to_numeric)
        data_covid.set_index('Date_reported',inplace=True)
        # data_covid.to_csv('offline_bulanan.csv')
        nat_group=data_covid.groupby('Country')
        with open('bulanan_last','w') as buka:
            buka.write(last_up)
    return nat_group, last_up
def update_data():
    long_lat=requests.get('https://raw.githubusercontent.com/darusdc/Mapping/master/gps_indonesia.json').json()
    r=requests.get('https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_Indonesia#Cases_by_province_and_region')
    soup=BeautifulSoup(r.content, 'html.parser')
    dataTarget=soup.find_all('table')
    columns=dataTarget[1].find_all('th')
    rows=dataTarget[1].find('tbody').find_all('tr')
    col_list=['img']
    with open('wikipedia_update','r') as last_update:
        dataoffline=last_update.read()
    if rows[-1].find('i').string == dataoffline :
        return rows[-1].find('i').string
    else:
        for i in columns:
            if i.string!=None:
                if '\n' in i.string:
                    col_list.append(i.string.replace('\n',''))
                else:
                    col_list.append(i.string)
        # col_list.remove('Index case(s)')
        rows_list=[]
        for i in range(3,len(rows)-2):
            prov=rows[i].th.find_all('a')[1].string
            conf=int(rows[i].find_all('td')[0].string.replace('\n'and',',''))
            recov=int(rows[i].find_all('td')[1].string.replace('\n'and',',''))
            death=int(rows[i].find_all('td')[2].string.replace('\n'and',',''))
            actv=int(rows[i].find_all('td')[3].string.replace('\n'and',',''))
            for x in long_lat:
                if rows[i].th.find_all('a')[1].string == x['Provinsi'] :
                    img=x['logo']
                    lng=x['longitude']
                    lat=x['latitude']
            rows_list.append([img,prov,conf,recov,death,actv,lat,lng])
        Data_Col_row=[]
        for x in rows_list:
            Data_Col_row.append({
                col_list[0]:x[0],
                col_list[1]:x[1],
                col_list[2]:x[2],
                col_list[3]:x[3],
                col_list[4]:x[4],
                'active':x[5],
                'lat':x[6],
                'long':x[7],
                })
        Data_Col_row=pd.DataFrame(Data_Col_row)
        Data_Col_row.to_csv('static/data_covid.csv')
        with open('wikipedia_update','w') as last_update:
            last_update.write(rows[-1].find('i').text.replace('[1]',''))
        return rows[-1].find('i').text.replace('[1]','')
def get_table():
    Data_Col_row=pd.read_csv('static/data_covid.csv').sort_values('active',ascending=False).reset_index()
    xax=[]
    for i in range(0,len(Data_Col_row['Province'])):
        xax.append(Data_Col_row['Province'][i])
    return list(xax)
def get_data():
    Data_Col_row=pd.read_csv('static/data_covid.csv').sort_values('active',ascending=False)
    return list(Data_Col_row['active'])
def color():
    return ("#"+str("".join([random.choice('0123456789ABCDEF') for x in range(6)])))
def image():
    Data_Col_row=pd.read_csv('static/data_covid.csv')
    sns.barplot(Data_Col_row['Province'],Data_Col_row['Confirmed'])
    plt.savefig('static/covid.png')
def show_map():
    ind_state=requests.get('https://raw.githubusercontent.com/darusdc/Mapping/master/indonesia-en.geojson').json()
    Data_Col_row=pd.read_csv('static/data_covid.csv')
    m=folium.Map(location=[-6.211544,106.845172],zoom_start=7)

    folium.Choropleth(
        ind_state,Data_Col_row,['Province','active'],
        key_on='feature.properties.state',
        legend_name='jumlah kasus Aktif di Indonesia',
        fill_color='OrRd', bins=3
    ).add_to(m)
    for i in range(len(Data_Col_row['Province'])):
        Icon=folium.CustomIcon(Data_Col_row['img'][i],icon_size=(32,32))
        folium.Marker([Data_Col_row['lat'][i],Data_Col_row['long'][i]],
        popup=f"<h3><B> {Data_Col_row['Province'][i]}: </B>{Data_Col_row['active'][i]}</h3><table><tbody><tr><th style='color:red'>Confirmed&nbsp;&nbsp;</th><th style='color:green'>Recovered&nbsp;&nbsp;</th><th style='color:black'>Deaths&nbsp;&nbsp;</th></tr><tr><td><center><b style='color:red'>{Data_Col_row['Cases'][i]}</b></center></td><td><center><b style='color:green'>{Data_Col_row['Recoveries'][i]}</b></center></td><td><center><b>{Data_Col_row['Deaths'][i]}</b></center></td></tr></tbody></table>",
        tooltip=f"<p><B> {Data_Col_row['Province'][i]}", icon=Icon).add_to(m)
    m.save("templates/covid2.html")