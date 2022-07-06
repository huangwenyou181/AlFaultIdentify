import os
from flask import jsonify, session, render_template, send_from_directory, url_for, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from application import db, app
from application.functions import generateTimeName, dbAddImage, process, detailReTab, getUserList, getDataAndDate
from application.models import User

UPLOAD_PATH = os.path.join(os.path.dirname(__file__))

@app.route("/")
@login_required
def index():
    print(current_user.is_authenticated)
    return render_template("index.html")

@app.route("/<filename>")
def rootfile(filename):
    return send_from_directory(UPLOAD_PATH, filename)

@app.route("/upImg", methods=["POST"])
def upImg():
    if request.method == 'POST':
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        new_name = generateTimeName() + '.jpg'
        savePath = os.path.join(url_for('static', filename='images/temp')+'/', new_name)
        f.save(basepath + savePath)
        id = dbAddImage(new_name, db, savePath, current_user.id)
        session["img_id"] = id
    return os.path.join('/', "test_new.jpg")

@app.route("/imgDownload", methods=["GET","POST"])
def imgDownload():
    imgId = session.get('img_id')
    return process(imgId, db)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.session.query(User).filter(User.name == username).first()
        
        if user is not None:
            check = user.valid_password(password)
            if check:
                login_user(user)
                return redirect(url_for('index'))
        
        flash('Invalid username or password.')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout(): 
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('login'))

@app.route('/charts', methods=["GET", "POST"])
@login_required
def charts():
    if request.method == 'POST':
        userid = current_user.id;
        re = detailReTab(userid, db);
        return jsonify(re)
    
    return render_template("charts.html")

@app.route('/grids', methods=["POST", "GET"])
@login_required
def grids():
    if request.method == 'POST':
        return jsonify(getUserList(current_user.id, db))

    return render_template("grids.html")

@app.route('/getGraphData', methods=["POST"])
@login_required
def getGraphData():
    uname = request.get_data()
    uname = str(uname, 'utf-8')
    return jsonify(getDataAndDate(uname, db))
