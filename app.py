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

@app.route('/login' , methods=['POST']) 
def login(): 
    loginUser = LoginUser(request.json.get('input'), request.json.get('password'))
    cursor = mydb.cursor()
    cursor.execute("SELECT ID,Username,Email,Paswort FROM Logins WHERE Username = %s OR Email = %s", (loginUser.input, loginUser.input))
    result = cursor.fetchone()
    if result:
        user = User(result[0], result[1], result[2], result[3])
        if user.password == loginUser.password:
            return 'Hallo' + user.username
        else:
            return 'WRONG Username or Password'
    else:
        return 'WRONG Username or Password'
    
if __name__=='__main__': 
   app.run(debug=True) 

   