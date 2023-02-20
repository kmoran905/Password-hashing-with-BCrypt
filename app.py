from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import shortuuid , securityhash , bcrypt
import MySQLdb.cursors
import re
  
  
app = Flask(__name__,template_folder='template')

#I have used https://www.freemysqlhosting.net/ to host a mySQL server
  
app.secret_key = 'apex'

#Configuration
app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql9596302'
app.config['MYSQL_PASSWORD'] = 'eFtTaecLY8'
app.config['MYSQL_DB'] = 'sql9596302'

  
mysql = MySQL(app)

#Instantiating the hash class to use the Hash function.
hashedString = securityhash.Hash()

#Using shortuuid to generate unique ids for users
id = shortuuid.uuid()

  
@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = 'Welcome'

    #Requesting the input fields for username and password
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Initializing the input fields and store them into variables
        username = request.form['username']
        password = request.form['password']

        #Connecting to mySQL database
        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #Fetching the user's hashed password 
        cursor1.execute('SELECT password FROM user WHERE username = %s' , (username, ))
        storedInDatabase = cursor1.fetchone()['password']

        #Checking if their account exists.
        cursor1.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, storedInDatabase,))

        #Initializing the user and storing in to a variable
        user = cursor1.fetchone()

        #Checking if password matches with the user's hashed password.
        checkpassword = bcrypt.checkpw(password.encode("utf-8") , storedInDatabase.encode("utf-8"))
        #If the user's account exists and the password is correct.
        if user and checkpassword: 
            #Login becomes sucessful        
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['username'] = user['username']
            message = 'Logged in successfully !'
            return render_template('user.html', message = message)
        else:
            message = 'Please enter correct username / password !'
    return render_template('login.html', message = message)

#Route to logging out of the user's account
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    message = 'Register your account'

    #Requesting the input fields for username and password
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Storing username input field to a variable
        username = request.form['username']

        #Hashing the user's chosen password 
        password = hashedString.hash(request.form['password'])

        #Connecting to mySQL database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #SELECT statement to see if the username already exists
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not username or not password:
            message = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO `user` VALUES (%s, %s, %s)', (id ,username, password))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message = message)
    
if __name__ == "__main__":
    app.run()