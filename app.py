from flask import Flask
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",    
    password="bMEM'16@22",
)

print(mydb)
     
app = Flask(__name__)  

@app.route('/')       
def hello(): 
    return 'HELLO'

  
if __name__=='__main__': 
   app.run(debug=True) 
   