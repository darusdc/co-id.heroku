import pandas as pd
import folium

mel=pd.read_csv('Melbourne_housing_FULL.csv')
region = mel['Regionname'].dropna(axis=0).unique()
mel.dropna(subset=['Price', 'Lattitude', 'Longtitude'], axis=0, inplace=True)
mel.drop('BuildingArea', axis=1, inplace=True)
from scipy.stats import mode
mode_room = []
for i in ['Bedroom2', 'Bathroom', 'Car', 'Landsize', 'YearBuilt']:
    mode_room.append(mode(mel[mel[i].isna()==True]['Rooms'])[0][0])
mode_df = pd.DataFrame(mode_room, index=['Bedroom2', 'Bathroom', 'Car', 'Landsize', 'YearBuilt'], columns=['mode_rooms'])
value_mode = []
for i in ['Bedroom2', 'Bathroom', 'Car', 'Landsize', 'YearBuilt']:
    value_mode.append(mode(mel[mel['Rooms'] == mode_df.mean()[0]][i])[0][0])
mode_df['value_mode'] = value_mode
na_columns = ['Bedroom2', 'Bathroom', 'Car', 'Landsize', 'YearBuilt']
for i in range(len(na_columns)):
    mel[na_columns[i]].fillna(mode_df['value_mode'][i], inplace=True)
listr=mel['Regionname'].unique()
listk=[i+1 for i in range(len(listr))]
dictr=dict(zip(listk,listr))
def Cyh(region='Southern Metropolitan', tenor=500):
    byreg=mel.groupby('Regionname')
    afford=byreg.get_group(region)[byreg.get_group(region)['Price']*1.5/240<=tenor]
    if len(afford)<=0:
        return False
    else:
        return afford
def show_map(afford=pd.DataFrame):
    afford.reset_index(inplace=True)
    tipe={'h':'house,cottage,villa, semi,terrace','u':'unit, duplex','t':'townhouse'}
    m= folium.Map(location=[afford['Lattitude'][0],afford["Longtitude"][0]],zoom_start=10)
    if len(afford)!=0:
        for i in range(len(afford)):
            folium.Marker(location=[afford['Lattitude'][i],afford['Longtitude'][i]], popup=f"daerah:<b> {afford['Suburb'][i]} </b> <p>tipe: <b>{tipe[afford['Type'][i]]}</b> <p><i>Harga: <b>{afford['Price'][i]}<b/></i></p><p>Cicilan: <b>{afford['Price'][i]*1.5/240}</b></p>",icon=folium.Icon(icon='home')).add_to(m)
        m.save('templates/rumah.html')
    else:
        print('data tidak boleh kosong')
def choice(dmn,tenor):
    if dmn=='':
        dmn=input('Masukkan no. region yang anda inginkan: ')
    if tenor=='':
        tenor=input('cicilan perbulan yang bisa anda bayarkan: ')
    hasil=Cyh(dictr[int(dmn)],int(tenor))
    if type(hasil) == pd.DataFrame:
        show_map(hasil)
    else:
        print(f"You can't afford any home with {tenor} budget in {dictr[int(dmn)]}, select another region")
        ch=input('do you want to change region or Q for exit? (Y/N/Q) ')
        if ch.lower()=='y':
            dmn=''
        elif ch.lower()=='q':
            print('thanks for using me :) see you later!')
        else:
            tenor=''
            choice(dmn,tenor)
