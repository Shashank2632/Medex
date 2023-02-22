from flask import Flask,render_template, request,redirect,url_for
from flask_mysqldb import MySQL
import os
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pharmacy'
 
mysql = MySQL(app)
picFolder = os.path.join('static', 'pics')

app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'a.jpg')
    return render_template("login.html", user_image=pic1)
    
@app.route('/login',methods=['POST','GET'])
def login():
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'a.jpg')
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'b.jpg')
    if request.method=='POST':
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM USER_DETAILS")
        mysql.connection.commit()
        cur.execute("SELECT * FROM login")
        mysql.connection.commit()
        name=cur.fetchall()
        cur.close()
        database = dict(name)
        name1=request.form['user']
        pwd=request.form['pass']
        if name1 not in database:
            return render_template('login.html',info='Invalid User', user_image=pic2)
        else:
            if database[name1]!=pwd:
                return render_template('login.html',info='Invalid Password', user_image=pic2)
            else:
                cur=mysql.connection.cursor()
                cur.execute("INSERT INTO USER_DETAILS(PID) VALUES(%s)",{name1})
                mysql.connection.commit()
                cur.close()
                return render_template('main.html', user_image=pic1)
    return render_template("login.html", user_image=pic2)
@app.route('/register',methods=['POST','GET'])
def register():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'b.jpg')
    if request.method=='POST':
        pat_id=request.form['pid']
        pwd=request.form['password']
        nam=request.form['na']
        address=request.form['addr']
        cont=request.form['con']
        pin=request.form['pin']
        cur=mysql.connection.cursor()

        cur.execute("INSERT INTO patient_details(PID,PASSWORD,Name,ADDRESS,PINCODE,CONTACT_NO) VALUES(%s,%s,%s,%s,%s,%s)",(pat_id,pwd,nam,address,pin,cont))
        mysql.connection.commit()
        cur.close()
        return render_template("login.html", user_image=pic1)
    return render_template("register.html", user_image=pic1)

@app.route('/data',methods=['POST','GET'])
def data():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'b.jpg')
    cur=mysql.connection.cursor()
    if request.method=='POST':
        med=request.form['medname']
        qty=int(request.form['quantity'])
        cur.execute("UPDATE drug_details SET QUANTITY=%s WHERE drug_details.DRUG_NAME=%s",{qty,med})
        mysql.connection.commit()
        cur.execute("UPDATE drug_details SET TOTAL=QUANTITY*PRICE")
        mysql.connection.commit()
        med1=med
        cur.execute("SELECT S.PHARMACY_NAME,S.ADDRESS,S.CONTACT_INFO FROM pharmacy_details S,stock_availability A,drug_details D WHERE S.PHAR_ID=A.PHAR_ID AND A.DRUG_NAME=%s AND D.QUANTITY<A.STOCK_REMAINING AND D.DRUG_NAME=%s ",(med,med1))
        mysql.connection.commit()
        name=cur.fetchall()
        cur.execute("SELECT DRUG_NAME,TOTAL FROM drug_details WHERE DRUG_NAME=%s",{med})
        name1=cur.fetchall()
        if not name1:
            cur.close()
            return render_template("main.html",data="INVALID DRUG NAME", user_image=pic1)
        if not name:
            cur.close()
            return render_template("main.html",data="INSUFFICIENT QUANTITY", user_image=pic1)
        else:
            cur.close()
            return render_template("data.html",data=name,data1=name1, user_image=pic1)  
    return render_template("main.html", user_image=pic1)
@app.route('/patient',methods=['POST','GET'])
def patient():
        pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'c.jpg')
        cur=mysql.connection.cursor()
        cur.execute("SELECT P.PID,Name,ADDRESS,CONTACT_NO FROM patient_details P,user_details U WHERE P.PID=U.PID")
        mysql.connection.commit()
        name=cur.fetchall()  
        cur.close()
        return render_template("patient.html",data=name, user_image=pic1) 
if __name__ == '__main__':
    app.run(debug=True,port=3307)


