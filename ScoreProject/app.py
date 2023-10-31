from flask import Flask, render_template, request, redirect
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session #import tools untuk website
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
db = SQL("sqlite:///score.db")
@app.route("/", methods=["GET", "POST"])
def index():
        if request.method == "POST": 
            name = request.form.get("name")
            score = request.form.get("score")

            db.execute("INSERT INTO score (name, score) VALUES(?, ?)", name, score)

            return redirect("/")
        else:

            students = db.execute("SELECT * FROM score")
            return render_template("index.html", students=students)
            
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_data(id):
    if request.method == "GET":
        score = db.execute("SELECT * FROM score WHERE id = ?", id)[0]
        print(score)
        return render_template("edit.html", score=score)
    elif request.method == "POST":
        score_name = request.form.get("name")
        score_score = request.form.get("score")
        db.execute('UPDATE score set name = ?, score = ? where id = ?', score_name, score_score, id)
        return redirect("/") 
               
@app.route("/delete/<id>", methods=["GET"])
def delete_id(id):
    db.execute("delete from score where id = ?", id)
    return redirect("/")    

@app.route("/register", methods=["GET", "POST"])
def register():
    
    """Register user"""
    # access form data (sesuaikan dengan form register masing-masing)
    if request.method == "POST":
        if not request.form.get("username"): 
            return "must provide username"
        elif not request.form.get("password"): 
            return "must provide password"
    # baca data username yang sudah terdaftar
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
    # baca data isian member baru dari form
        username = request.form.get("username")
        password = request.form.get("password")
        password_repeat= request.form.get("confirmation")
    # enkripsi password
        hash = generate_password_hash (password)
        if len(rows) == 1: # jika ditemukan username yang sama
            return "username already taken"
        if password == password_repeat: # jika password = ulang password    
# masukkan data member baru db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
    # ambil data user baru dan simpan pada session You, 
            db.execute("INSERT INTO users (username, hash) VALUE(?, ?)", username, hash)
            registered_user = db.execute("select * from users where username = ?", username)
            session["user_id"] = registered_user[0]["id"] 
            flash('You were successfully registered') # notifikasi 
            return redirect("/")
        else:

# jika password dan ulangi password tidak cocok return "must provide matching password"
            return render_template("register.html", userdb=userdb)

    else:
        return render_template("register.html")