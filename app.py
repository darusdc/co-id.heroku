from flask import Flask, render_template, url_for, jsonify, abort, make_response, redirect,request
# from form import RegistrationForm
import showmap
# from flask_cors import CORS
import pandas as pd
import seaborn as sns
#import chome
app=Flask(__name__)
# CORS(app)
app.config['SECRET_KEY']='eb548ce03fbe2e738e916a3497aa6024'
Students = [
    {
        'id': 1,
        'name': 'Andi',
        'age': 21
    },
    {
        'id': 2,
        'name': 'Budi',
        'age': 22
    },
    {
        'id': 1,
        'name': 'Caca',
        'age': 23
    }
]
lomba=['lkbb','sc','maket']
posts=[
    {
        'author':'Muhammad Darussalam',
        'title': 'Dashboard by Darus',
        'content':'first post content',
        'date_posted': 'April 20,2020'
    },
    {
        'author':'Richard miles',
        'title': 'Dashboard by richard',
        'content':'first post content',
        'date_posted': 'April 20,2020'
    },
    {
        'author':'Richard miles',
        'title': 'Dashboard by richard',
        'content':'first post content',
        'date_posted': 'April 20,2020'
    },

]

@app.route(f'/mata_lomba')
def matlom():
    result=''
    for i in lomba:
        if result=='':
            result+='<p>'+i+'</p>'
        else:
            result+='<p>' +i +'</p>'
    return f"<h1> {result} <h1>"

@app.route('/')
def index():
    colors=[showmap.color() for x in range(34)]
    update=showmap.update_data()
    return render_template('index.html', update=update, posts=posts,active='Dashboard',prov=showmap.get_table(),jum=showmap.get_data(),col=colors,covids=zip(showmap.get_table(),showmap.get_data(),colors))
@app.route('/about')
def about():
    return render_template('about.html')
# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     return render_template('register.html', title='Register', form=form)
@app.route('/covid')
def covid():
    showmap.show_map()
    return render_template('covid.html', title='Data Covid Indonesia',active='covid')
@app.route('/covid2')
def covid2():
    return render_template('covid2.html', title='Data Covid Indonesia',active='covid')
 
@app.route('/kasus_baru')
def new_cases():
    kb,update=showmap.data_bulanan()
    negara=list(kb.groups)
    month=list(kb.get_group('Indonesia').resample('M').mean().index.month_name())
    cases=list(round(kb.get_group('Indonesia').resample('M').mean()['New_cases']))
    death=list(round(kb.get_group('Indonesia').resample('M').mean()['New_deaths']))
    return render_template('kasus.html',update=update,active='Bulanan',data=kb,deaths=death,country=negara,month=month,cases=cases,col=[showmap.color() for x in range(5)])
# @app.route('/home')
# def home():
#     return render_template('home.html', title='cari rumah', active='home')
@app.route('/home2')
def home2():
    return render_template('home2.html', title='cari rumah', active='home')
@app.route('/data', methods=['GET','POST'])
def data():
    if request.method=='POST':
        body=request.json
        print(body['name'])
        # print(body)

        return jsonify({'name':body['name'],'age':body['age']})
    else:
        return jsonify({'status': 'you are getting!'})


@app.route('/data/<int:id>')
def datas(id):
    if id <1 or id> len(Students):
        abort(404)
    else:
        return jsonify(Students[id-1])
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'status':'Error not found!'}),404)

@app.route('/search')
def search():
    print(request.args)
    print(request.args['keyword'])
    return request.view_args
if __name__== "__main__":
    app.run(debug=True)