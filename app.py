from flask import Flask, render_template,request,redirect,url_for,session,flash
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 

app = Flask(__name__)

app.secret_key='vaishnavi'
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="Amazon_clone_website"
mysql=MySQL(app)    


    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/seemore')
def seemore():
    
    return render_template('seemore.html')

@app.route('/admin')
def admin():
        if 'username' in session:
            return render_template('admin.html',username=session['username'])


       
        
@app.route('/login',methods=['POST','GET'])
def login():
        if request.method == 'POST':
            username=request.form['username']
            pwd=request.form['password']
            Role=request.form['Role']
            cur=mysql.connection.cursor()

            cur.execute("SELECT * FROM users  WHERE username=%s And password=%s And Role=%s ",(username,pwd,Role))
            user=cur.fetchone()
            cur.close()
            if user:
                session['username']=user[2]
                session['password']=user[3]
                session['Role']=user[5]
                if Role=='Admin':
                     return redirect(url_for('admin'))
                else:
                     return redirect(url_for('custmor'))
                
            else :     
                     return render_template('login.html',error='Invalid username or password')
        return render_template('login.html')   

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and  'username' in request.form and 'password' in request.form and 'email' in request.form and 'name' in request.form and 'role' in request.form:
        name=request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        Role=request.form['role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s)', (name,username,password, email,Role))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


                             # *********Insert Menu*********

@app.route('/seemore', methods =['GET', 'POST'])
def add_product():
   
        
    if request.method == 'POST': 
    # and  'event_name' in request.form and 'email' in request.form and 'date' in request.form and 'mobile' in request.form and 'amobile' in request.form  and 'amount' in request.form  and 'des' in request.form:
        msg = 'data inserted sucessfully'  
        product_id = request.form['product_id']  
        product_name = request.form['product_name'] 
        product_quantity = request.form['product_quantity']            
        cursor = mysql.connection.cursor()
             
        cursor.execute('INSERT INTO add_product (product_id, product_name, product_quantity ) VALUES ( %s, %s, %s)', 
                       (product_id, product_name, product_quantity))
        mysql.connection.commit()
        flash("your record has been submitted successfully", "success")
    return render_template('seemore.html',msg=msg)

                          # ********* Delete Menu*********

@app.route('/delete/<string:product_id_data>', methods = ['GET'])
def delete(product_id_data):
    msg = ("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM add_product WHERE product_id=%s", (product_id_data,))
    mysql.connection.commit()
    return render_template('seemore.html')

                                   
    
if __name__=="__main__":
  app.run(debug=True)