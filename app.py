from flask import Flask, request
import mysql.connector 
import uuid
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime , timedelta

mydb = mysql.connector.connect(host="localhost",user="root",password=input("passwort:"),database="Logininfo")  
app = Flask(__name__)  

class User:
    def __init__(self,UID, username,email, password):
        self.UID = UID
        self.username = username 
        self.email = email
        self.password = password

class LoginUser:
    def __init__(self,input, password):
        self.input = input
        self.password = password

class Token:
    def __init__(self,token,UID):
        self.UID = UID
        self.token = token
    
def generate_token(UID, secret_key):
    payload = {
        'UID': UID,
        'exp':  datetime.utcnow()  + timedelta(hours=1)
    }   
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    with mydb.cursor() as cursor:
        cursor.execute("INSERT INTO Token (UID,Token,Time) VALUES (%s, %s, %s)", (UID, token, datetime.utcnow() ))
        mydb.commit()
    return token

    
def DBdata(Username,Email):
    with mydb.cursor() as cursor:
        if Email == None:
            cursor.execute("SELECT UID,Username,Email,Password FROM Logins WHERE Email = %s", (Email,))
        else:
            cursor.execute("SELECT UID,Username,Email,Password FROM Logins WHERE Username = %s", (Username,))
        return cursor.fetchone()

@app.route('/login' , methods=['POST']) 
def login(): 
    loginUser = LoginUser(request.json.get('input'), request.json.get('password'))
    result = DBdata(loginUser.input,loginUser.input)
    if result:
        user = User(result[0], result[1], result[2], result[3])
        if check_password_hash(user.password, loginUser.password):
            generate_token(user.UID, user.password)
            return 'Hallo ' + user.username + ' , but your token is expired, a new one has been generated'
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
            hashed_password = generate_password_hash(registerUser.password , 'pbkdf2:sha256')
            sql = "INSERT INTO Logins (UID,Username, Email, Password) VALUES (%s, %s, %s, %s)"
            val = (str(uuid.uuid4()),registerUser.username, registerUser.email, hashed_password)
            cursor.execute(sql, val)
            mydb.commit()
            return 'Registration successful'
        
@app.route('/', methods=['POST'])
def Jwt():
    logintoken = request.json.get('token')
    with mydb.cursor() as cursor:
        cursor.execute("SELECT UID,Token FROM token WHERE Token = %s", (logintoken,))
        oken = cursor.fetchone()
        if oken is None:
            return 'Token is invalid'
        token = Token(oken[1], oken[0])
        cursor.execute("UPDATE Token SET Time = %s WHERE Token = %s", (datetime.utcnow() ,logintoken))
        mydb.commit()
        return 'Token is valid'
    
    if __name__=='__main__': 
        app.run(debug=True)
