#Import Library
from flask import Flask, render_template, url_for, jsonify, abort, make_response, redirect,request
import showmap
import pandas as pd
import seaborn as sns

#Booting up
app=Flask(__name__)
app.config['SECRET_KEY']='eb548ce03fbe2e738e916a3497aa6024'
kb,update=showmap.data_bulanan()
update=showmap.update_data()

#Routing
@app.route('/')
def index():
    return render_template('index.html', update=update,active='Dashboard')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/covid')
def covid():
    showmap.show_map()
    return render_template('covid.html', title='Data Covid Indonesia',active='covid')
@app.route('/covid2')
def covid2():
    return render_template('covid2.html', title='Data Covid Indonesia',active='covid')
 
@app.route('/kasus_baru')
def new_cases():
    # month=list(kb.get_group('Indonesia').resample('M').mean().index.month_name())
    # cases=list(round(kb.get_group('Indonesia').resample('M').mean()['New_cases']))
    # death=list(round(kb.get_group('Indonesia').resample('M').mean()['New_deaths']))
    return render_template('kasus.html',update=update, active='Bulanan',country = kb ,col=[showmap.color() for x in range(5)])

if __name__== "__main__":
    app.run(debug=True)