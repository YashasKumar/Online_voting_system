import mysql.connector
import matplotlib.pyplot as plt
import datetime
import re

con=mysql.connector.connect(host="localhost",user="root",passwd="Akhilesh1327$l",database="it_project")
cursor=con.cursor()
from flask import Flask, redirect, request,render_template

app=Flask(__name__)

input_date = datetime.datetime(2023,11,8,16,55,0)
@app.route('/', methods=['POST','GET'])
def login():
    if request.method=='POST':
        global email
        email=request.form['email']
        password=request.form['password']
        sql="select email,passwd from voter_details"
        sql1="select email,passwd from admin_details"
        cursor.execute(sql)
        data=cursor.fetchall()
        cursor.execute(sql1)
        data1=cursor.fetchall()
        if (email,password) in data:
            return render_template('voter.html')
        elif (email,password) in data1:
            return render_template('admin.html')       
        return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/login_page/')
def login_page():
    return render_template('login.html')

@app.route('/signup_page/')
def signup_page():
    return render_template('signup.html')

def is_valid_email(email):
    # Check if the email matches a specific pattern using regular expressions
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email)

@app.route('/signup/',methods=['POST','GET'])
def signup():
        if request.method=='POST':
            email=request.form['email']
            password=request.form['password']
            roll=request.form.get('roll')
            name=request.form.get('name')    
            # Perform validation
            errors = []
            if not email or not is_valid_email(email):
                errors.append('Please enter a valid email address')
            if not roll:
                errors.append('Roll is required')
            if not name:
                errors.append('Name is required')
            if not password or len(password) < 8:
                errors.append('Password must be at least 8 characters long')
            if errors:
                return render_template('signup.html')
            sql="insert into voter_details(roll_no,full_name,email,passwd) values('{}','{}','{}','{}')".format(roll,name,email,password)   
            cursor.execute(sql)
            con.commit()
            return render_template('login.html')
        else:
            return render_template('signup.html')

# @app.route('/signup/',methods=['POST','GET'])
# def signup():
#         if request.method=='POST':
#             email=request.form['email']
#             password=request.form['password']
#             roll=request.form.get('roll')
#             name=request.form.get('name')
#             sql="insert into voter_details(roll_no,full_name,email,passwd) values('{}','{}','{}','{}')".format(roll,name,email,password)   
#             cursor.execute(sql)
#             con.commit()
#             return render_template('login.html')
#         else:
#             return render_template('signup.html')

@app.route('/add_candidate/',methods=['POST','GET'])
def add_candidate():
    if request.method=='POST':
        email=request.form['email']
        phone_number=request.form['phone']     
        roll=request.form['roll']
        name=request.form['name']
        bio=request.form['bio']
        # Perform validation
        errors = []
        if not email or not is_valid_email(email):
            errors.append('Please enter a valid email address')
        if not roll:
            errors.append('Roll is required')
        if not name:
            errors.append('Name is required')
        if not bio:
            errors.append("Bio is needed")
        if errors:
            return render_template('add_candidate.html')
        sql="insert into candidate_details(roll_no,full_name,email,phone_number,about) values('{}','{}','{}',{},'{}')".format(roll,name,email,phone_number,bio)
        cursor.execute(sql)
        con.commit() 
        return render_template('admin.html')
    else:
        return render_template('add_candidate.html')

@app.route('/candidate_details/',methods=['POST','GET'])
def candidate_details():
        sql="select * from candidate_details"
        cursor.execute(sql)
        data=cursor.fetchall()
        return render_template('candidate_details.html',data=data)

@app.route('/delete/<string:roll>',methods=['POST','GET'])
def delete_candidate(roll):
    sql="delete from candidate_details where roll_no='{}'".format(roll)
    cursor.execute(sql)
    con.commit()
    return redirect('/candidate_details')

@app.route('/voter_candidate_details',methods=['GET','POST'])   
def voter_candidate_details():
    current_date = datetime.datetime.now()  # Get the current date
    global input_date
    if current_date < input_date:
        sql="select * from candidate_details"
        cursor.execute(sql)
        data=cursor.fetchall()
        sql3="select vote from voter_details where email='{}'".format(email)
        cursor.execute(sql3)
        data1=cursor.fetchall()
        if (data1[0][0]==1):
            return redirect('/post_vote_candid')
        return render_template('voter_candidate_details.html',data=data)
    else:
        return redirect('/post_vote_candid')
@app.route('/voter/',methods=['POST','GET'])
def voter():
    return render_template('voter.html')

@app.route('/update/<string:roll>',methods=['POST','GET'])
def update_vote(roll):
    if request.method == 'POST':
        return render_template('voter.html')
    else:
        sql="select votes from candidate_details where roll_no='{}'".format(roll)
        cursor.execute(sql)
        old_vote=cursor.fetchall()
        sql2="update candidate_details set votes={} where roll_no='{}'".format(int(old_vote[0][0])+1,roll)
        cursor.execute(sql2)
        sql4="update voter_details set vote={} where email='{}'".format(1,email)
        cursor.execute(sql4)
        con.commit()
        return redirect('/voter/')

@app.route('/post_vote_candid',methods=['POST','GET'])
def post_vote_candid_details():
    sql="select * from candidate_details"
    cursor.execute(sql)
    data=cursor.fetchall()
    return render_template('post_vote_candid.html',data=data)

@app.route('/logout/')
def logout():
    return render_template('login.html')

@app.route('/result')
def result():
    global input_date # Convert input date to datetime object
    current_date = datetime.datetime.now()  # Get the current date

    if current_date > input_date:
        sql = "select full_name from candidate_details "
        cursor.execute(sql)
        candid = cursor.fetchall()
        candidates=[]
        for cand in candid:
            candidates.append(*cand)
        sql1="select votes from candidate_details"
        cursor.execute(sql1)
        votes_ = cursor.fetchall()
        votes=[]
        for vote in votes_:
            votes.append(*vote)
        winner_index = votes.index(max(votes))
        explode = [0.2 if i == winner_index else 0 for i in range(len(candidates))]
        plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(votes, labels=candidates, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'], explode=explode, shadow=True)
        plt.legend(wedges, candidates, title="Candidates", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.axis('equal')
        plt.savefig('static/my_plot.png', bbox_inches='tight')
        sql1="select full_name from candidate_details where votes = (select max(votes) from candidate_details)"
        cursor.execute(sql1)
        data=cursor.fetchall()
        return render_template('result.html', data=data)
    else:
        return "Results will be available after the input date."
if __name__=="__main__":
    app.run(debug="True")
