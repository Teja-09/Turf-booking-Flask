from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json


app = Flask(__name__)

account_database = json.load(open("databases/accounts.json", "r"))

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "You have already logged in... <a href='/logout'>Logout</a>"

@app.route('/register', methods=['GET','POST'])
# Storeing register details
def register():
    if request.method == 'POST':
        email = request.form['email']
        uname =  request.form['username']
        passw = request.form['password']   
        role = request.form['role']       
        print(uname + " " + passw + ' ' + email + " " + role)

        if uname not in account_database['users']:
            uid = len(account_database['users'])
    
            account_database['accounts'][uid] = {
                "email" :email,
                "username": uname,
                "password": passw,
                "designation": role 
            }
    
            account_database['users'].append(uname)

            json.dump(account_database, open("databases/accounts.json", "w"))

            flash('Registration successfully, plz login.')
            return home()
        else:
            return("User name or email already exists.. Please try some other.")
    else:
        return render_template('registration.html')


@app.route('/login', methods=['GET','POST'])
# Login auth
def login():
    if request.method == 'POST':
        uname =  request.form['uname']
        passw = request.form['password']  

        if uname in account_database['users']:
            uid = str(account_database['users'].index(uname))
            if passw == account_database['accounts'][uid]['password']:
                if account_database['accounts'][uid]['designation'] == 'User' or account_database['accounts'][uid]['designation'] == 'Manager':
                    return render_template('user.html', result = account_database['prices'], name = uname)
                else:
                    return render_template('admin.html', result = account_database['prices'], name= uname)

        
        return "Login failed!! Check credentials"


@app.route('/addTurf', methods=['GET','POST'])
def addTurf():
    if request.method == 'POST':
        turfname = request.form['turf']
        cost = request.form['cost'] 

        loadname = str(turfname)
        account_database['prices'][loadname] = str(cost)

        json.dump(account_database, open("databases/accounts.json", "w"))
 
        print(turfname + " " + cost)
        return render_template('admin.html', result = account_database['prices'])

  
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
