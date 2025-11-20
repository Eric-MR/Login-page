from flask import Flask, request
import mysql.connector 

mydb = mysql.connector.connect(host="localhost",user="root",password="bMEM'16@22",database="Logininfo")  
app = Flask(__name__)  

class User:
    def __init__(self,ID, username,email, password):
        self.ID = ID
        self.username = username 
        self.email = email
        self.password = password

class LoginUser:
    def __init__(self,input, password):
        self.input = input
        self.password = password

def DBdata(Username,Email):
    with mydb.cursor() as cursor:
        if Email == None:
            cursor.execute("SELECT ID,Username,Email,Paswort FROM Logins WHERE Email = %s", (Email,))
        else:
            cursor.execute("SELECT ID,Username,Email,Paswort FROM Logins WHERE Username = %s", (Username,))
        return cursor.fetchone()

@app.route('/login' , methods=['POST']) 
def login(): 
    loginUser = LoginUser(request.json.get('input'), request.json.get('password'))
    result = DBdata(loginUser.input,loginUser.input)
    if result:
        user = User(result[0], result[1], result[2], result[3])
        if user.password == loginUser.password:
            return 'Hallo' + user.username
        else:
            return 'WRONG Username or Password'
    else:
        return 'WRONG Username or Password'
@app.route('/register' , methods=['POST'])
def register(): 
    registerUser = User(None, request.json.get('username'), request.json.get('email'), request.json.get('password'))
    with mydb.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Logins WHERE Username = %s)", (registerUser.username,))
        username_exists = cursor.fetchone()[0]
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Logins WHERE Email = %s)", (registerUser.email,))
        email_exists = cursor.fetchone()[0]
        if username_exists:
            return 'Username already exists'
        if email_exists:
            return 'Email already exists'
        else:
            sql = "INSERT INTO Logins (Username, Email, Paswort) VALUES (%s, %s, %s)"
            val = (registerUser.username, registerUser.email, registerUser.password)
            cursor.execute(sql, val)
            mydb.commit()
            return 'Registration successful'

if __name__=='__main__': 
   app.run(debug=True) 

   