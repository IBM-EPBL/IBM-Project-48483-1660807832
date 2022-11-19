from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=kbw87037;PWD=NpL74VJhIH9uRhtO","","")

#login page
@app.route('/login',methods=['GET',"POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user_name = request.form.get('uname')
        password = request.form.get('password')
        # print(user_name,password)
        
        query = ibm_db.exec_immediate(conn,"SELECT UNAME,PASSWORD FROM USERS WHERE UNAME='"+user_name+"'")
        results = ibm_db.fetch_both(query)
        # print(results)
        if results:
            # print(password,results['PASSWORD'])
            if results["PASSWORD"].strip() == password:
                print(password)
                return redirect(url_for('home'))    
        return redirect(url_for('login'))

#sign up page
@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    if request.method == 'POST':
        user_name = request.form.get('uname')
        password = request.form.get('password')
        email = request.form.get('email')
        # print(user_name,password,email)
        query = ibm_db.exec_immediate(conn, "INSERT INTO USERS VALUES ('"+ user_name+"','"+email+"','"+password+"')")
        
        return redirect(url_for('login'))


#update
@app.route('/update',methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        myquery = "UPDATE DATA SET QUANTITY='"+str(request.form.get('qty'))+"' WHERE SNAME='"+str(request.form.get('sname'))+"';"
        stmt = ibm_db.exec_immediate(conn, myquery)
        return redirect(url_for('home'))

#delete
@app.route('/delete')
def delete():
    print(request.args.get('sname'))
    stmt = ibm_db.exec_immediate(conn, "delete from DATA where SNAME='"+request.args.get('sname')+"';")

    return redirect(url_for('home'))

#add
@app.route('/add',methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        sname = request.form.get('sname')
        qty = request.form.get('qty')

        query = ibm_db.exec_immediate(conn, "INSERT INTO DATA VALUES ('"+ sname+"','"+str(qty)+"')")
          

        return redirect(url_for('home'))


#home
@app.route('/home',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        query = ibm_db.exec_immediate(conn,"SELECT * FROM DATA")
        data_arr = []
        while ibm_db.fetch_row(query) !=  False:
            data_arr.append({"sname":ibm_db.result(query, 0).strip(),"qty":ibm_db.result(query, 1)})
        print(data_arr)
        return render_template('home.html',data = data_arr)
    


if __name__ == '__main__':
    app.run(host = 'localhost',port = 5000,debug = True)