# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from bs4 import BeautifulSoup
import requests
import re
import random
import urllib

# Function to load data
def data_bulanan():

    #Load and Processing Data from WHO
    last_update=requests.get('https://covid19.who.int/')
    last_update = BeautifulSoup(last_update.content,'html.parser')
    last_up=last_update.find_all('h2')[1].find_all('span')[1].text
    # last_up=last.split(': ')[1].split(',')
    # last_up=' '.join(last_up)
    write = False

    # Check if data is newest
    with open('bulanan_last','r') as baca:
        data_offline=baca.read()
    
    if last_up!=data_offline :
        print('if')
        # data=pd.read_csv('offline_bulanan.csv')
        # data['Date_reported']=data['Date_reported'].apply(pd.to_datetime)
        # data[['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']] = data[['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']].apply(pd.to_numeric)
        # data.set_index('Date_reported',inplace=True)
        # # data.drop('Unnamed 1:',axis =1,inplace=True)
        # nat_group=data.groupby('Country')
    # Load data if there is new database
    # else:
        print('else')
        urllib.request.urlretrieve('https://covid19.who.int/WHO-COVID-19-global-data.csv','offline_bulanan.csv')
        data_covid=pd.read_csv('offline_bulanan.csv')
        data_covid['Date_reported']=data_covid['Date_reported'].apply(pd.to_datetime)
        data_covid[['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']] = data_covid[['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']].apply(pd.to_numeric)
        data_covid.set_index('Date_reported',inplace=True)
        # data_covid.to_csv('offline_bulanan.csv')
        nat_group=data_covid.groupby('Country')
        with open('bulanan_last','w') as buka:
            buka.write(last_up)
        write = True
    Country_JS=dict()
    print(write)
    # Change format data to JSON
    
    # Write it to data.js for accessible data
    if write:
        for i in list(nat_group.groups):
            Country_JS[i]= {
                'data_m': [round(x) for x in nat_group.get_group(i).resample('M').mean()['New_deaths']],
                'data_h': [round(x) for x in nat_group.get_group(i).resample('M').mean()['New_cases']]
            }
        month = nat_group.get_group('Indonesia').resample('M').mean().index.to_period('M')
        cases = [round(x)  for x in nat_group.get_group('Indonesia').resample('M').mean()['New_cases']]
        death = [round(x)  for x in nat_group.get_group('Indonesia').resample('M').mean()['New_deaths']]
        with open('./static/assets/js/data.js','w') as js:
            js.write("\
                var ctx = document.getElementById('linePlot');\n\
                var linePlot= new Chart(ctx, {\n\
                    type: 'line',\n\
                    data: {\n\
                        labels: ["+", ".join([f'"{i}"' for i in month])+"],\n\
                        datasets: [{\n\
                            label: 'New Deaths',\n\
                            data: "+ str(death) +" ,\n\
                            backgroundColor: '#fc0703',fill: true\n\
                        }, {\n\
                            label: 'New Cases',\n\
                            data: "+ str(cases) +" ,\n\
                            backgroundColor: '#fcd303',fill: true\n\
                        }]\n\
                    },\n\
                    options:{\n\
                        responsive: true,\n\
                        tooltips: {mode: 'index',intersect: false,},\n\
                        hover: {mode:'nearest',intersect:true},\n\
                        scales:{\n\
                            xAxes: [{\n\
                                scaleLabel:{\n\
                                    display:true,\n\
                                    labelString:'Month'\n\
                                }\n\
                            }],\n\
                            yAxes:[{\n\
                                display: true,\n\
                                scaleLabel:{\n\
                                    display: true,\n\
                                    labelString:'# Cases'\n\
                                }\n\
                            }]\n\
                        }\n\
                    }\n\
                });\n\
                var data_base= \
                " + str(Country_JS) + ";\n\
                document.getElementById('negara').onchange = function(){\n\
                    var plot = linePlot.config.data;\n\
                    var neg = document.getElementById('negara').value;\n\
                    plot.datasets[0].data=data_base[neg]['data_m'];\n\
                    plot.datasets[1].data=data_base[neg]['data_h'];\n\
                    document.getElementById('judul').innerHTML=neg;\n\
                    linePlot.update()\n\
                };"
                    )
    country = ['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia (Plurinational State of)', 'Bonaire', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'C\\xc3\\xb4te d\\xe2\\x80\\x99Ivoire', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Cura\\xc3\\xa7ao', 'Cyprus', 'Czechia', "Democratic People\\'s Republic of Korea", 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo[1]', 'Kuwait', 'Kyrgyzstan', "Lao People\\'s Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia (Federated States of)', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'North Macedonia', 'Northern Mariana Islands (Commonwealth of the)', 'Norway', 'Oman', 'Other', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'R\\xc3\\xa9union', 'Republic of Korea', 'Republic of Moldova', 'Romania', 'Russian Federation', 'Rwanda', 'Saba', 'Saint Barth\\xc3\\xa9lemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Eustatius', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'T\\xc3\\xbcrkiye', 'Tajikistan', 'Thailand', 'The United Kingdom', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Republic of Tanzania', 'United States Virgin Islands', 'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe', 'occupied Palestinian territory, including east Jerusalem']
    return country, last_up

#Load Data from wikipedia
def update_data():
    # Request for new update data
    long_lat=requests.get('https://raw.githubusercontent.com/darusdc/Mapping/master/gps_indonesia.json').json()
    r=requests.get('https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_Indonesia#Cases_by_province_and_region')
    soup=BeautifulSoup(r.content, 'html.parser')
    dataTarget=soup.find_all('table')
    columns=dataTarget[0].find_all('th')
    rows=dataTarget[0].find('tbody').find_all('tr')
    col_list=['img']
    
    #Check if there any newest data
    with open('wikipedia_update','r') as last_update:
        dataoffline=last_update.read()
    #if no new data, so the data will be drag from offline data
    if rows[-1].find('i').string == dataoffline :
        Data_Col_row = pd.read_csv("static/data_covid.csv")
    else:
    # New data grabbed
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
        # Write to new offline data
        Data_Col_row.to_csv('static/data_covid.csv')
        with open('wikipedia_update','w') as last_update:
            last_update.write(rows[-1].find('i').text.replace('[1]',''))
    province = list(Data_Col_row.sort_values('active',ascending=False)['Province'])
    jum = list(Data_Col_row.sort_values('active',ascending=False)['active'])
    colors=[color() for x in range(34)]

    # Write new data to javascript for accessibility
    with open('./static/assets/js/data_indo.js','w') as js:
        js.write("\
        var ctx=document.getElementById('barPlot');\
        var dtx=document.getElementById('vbarPlot');\
        var etx=document.getElementById('piePlot');\
        var source = {\
                            labels: "+ str(province) +",\
                            datasets: [{\
                                label:' # Active cases',\
                                data: "+ str(jum) +",\
                                backgroundColor: "+ str(colors) +",\
                                borderWidth:1\
                            }]\
                        };\
        var option={\
                        animation: {\
                        onComplete: () => {\
                        delayed = true;\
                    },\
                    delay: (context) => {\
                        let delay = 0;\
                        if (context.type === 'data' && context.mode === 'default' && !delayed) {\
                            delay = context.dataIndex * 300 + context.datasetIndex * 100;\
                        }\
                    return delay;\
                    },\
                    },\
                    responsive: true,\
                    legend: {\
                        position: 'right',\
                    },\
                    title: {\
                        display: true,\
                        text: 'Rank of Active Cases by Province'\
                    }\
                };\
                    var barPlot= new Chart(ctx, {\
                        type: 'horizontalBar',\
                        data: source,\
                        options: option\
                    });\
                    var vbarPlot= new Chart(dtx, {\
                        type: 'bar',\
                        data: source,\
                        options: option\
                    });\
                    var piePlot= new Chart(etx, {\
                        type: 'pie',\
                        data: source,\
                        options: option\
                    });    ")
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
# Map Generator
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