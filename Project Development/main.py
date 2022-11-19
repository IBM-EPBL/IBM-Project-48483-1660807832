from flask import Flask,render_template,request,redirect,url_for
app = Flask(_name_)

#login page
@app.route('/login',methods=['GET',"POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        
        return redirect(url_for('login'))

#sign up page
@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    if request.method == 'POST':
        
        return redirect(url_for('login'))


if _name_ == '_main_':
    app.run(host = 'localhost',port = 5000,debug = True)
