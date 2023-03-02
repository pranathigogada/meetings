from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

from datetime import datetime

app=Flask(__name__)

app.config['MYSQL_HOST']="127.0.0.1"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="Bindu@123"
app.config['MYSQL_DB']="flaskapp"

mysql=MySQL(app)

ongoings=1000
ongoing_names=[]

message=""

def check_timings(start,end):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    for i in range(len(ongoing_names)):
        cur.execute('SELECT start_time,end_time FROM ongoing WHERE p_name=%s',(ongoing_names[i],))
        temp=cur.fetchall()

        if temp:
            for temp1 in temp:
                start_time=temp1['start_time'];end_time=temp1['end_time']
                start=datetime.strptime(str(start),'%H:%M:%S').time()
                end=datetime.strptime(str(end),'%H:%M:%S').time()
                start_time=datetime.strptime(str(start_time), '%H:%M:%S').time()
                end_time=datetime.strptime(str(end_time), '%H:%M:%S').time()

                if (start>start_time and start<end_time) or (end>start_time and end<end_time):
                    return False,ongoing_names[i]
                else:
                    continue
    return True,None

        

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/schedule',methods=['GET','POST'])
def schedule():
    global ongoing_names
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM participants')
    details=cur.fetchall()
    cur.close()

    if request.method=='POST':
        names=request.form.getlist('name')
        if len(names)>2:
            ongoing_names=names.copy()
            return redirect(url_for('timings'))
        else:
            message="Participants should be greater than 2"
            return render_template('error.html',message=message)

    return render_template('schedule.html',details=details)


@app.route('/timings',methods=['GET','POST'])
def timings():
    global ongoing_names
    global ongoings
    dates=request.form
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
        result,name=check_timings(dates['start'],dates['end'])
        if result:
            for i in range(len(ongoing_names)):
                cur.execute('SELECT p_id FROM participants WHERE p_name=%s',(ongoing_names[i],))
                p_id=cur.fetchone()['p_id']
                cur.execute("INSERT INTO ongoing VALUES (%s,%s,%s,%s,%s)",(ongoings,p_id,ongoing_names[i],dates['start'],dates['end']))
            mysql.connection.commit()
            ongoings+=5
            ongoing_names.clear()
            cur.close()
            return render_template('index.html')
        else:
            message=str(name)+" already in meeting"
            return render_template('error.html',message=message)

    return render_template('timings.html')


@app.route('/ongoing_interviews')
def ongoing_interviews():
    names={};timing={}
    ids_list=[]
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT DISTINCT(o_id) FROM ongoing')
    ids=cur.fetchall()
    for i in ids:
        ids_list.append(i['o_id'])
    for i in ids_list:
        cur.execute('SELECT p_name FROM ongoing WHERE o_id=%s',(i,))
        temp=cur.fetchall()
        temp_list=[]
        cur.execute('SELECT start_time,end_time FROM ongoing WHERE o_id=%s',(i,))
        temp1=cur.fetchone()
        start=temp1['start_time'];end=temp1['end_time']
        timing[i]=[start,end]
        for j in temp:
            temp_list.append(j['p_name'])
        names[i]=temp_list

    return render_template('ongoing_interviews.html',names=names,timing=timing)


@app.route('/edit',methods=['GET','POST'])
def edit():
    return render_template('edit.html')

if __name__=="__main__":
    app.run(debug=True)