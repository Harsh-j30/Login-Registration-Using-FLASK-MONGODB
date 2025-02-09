from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flash messages
app.config["MONGO_URI"] = "mongodb://localhost:27017/Flask_Users"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)



@app.route('/')
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        

        if not name or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("register"))

        # Check if email already exists
        if mongo.db.fusers.find_one({"email": email}):
            flash("Email already registered!", "warning")
            return redirect(url_for("register"))
        
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert user into MongoDB
        mongo.db.fusers.insert_one({"name": name, "email": email, "password": hashed_pw})

        flash("Registration successful! You can now login.", "success")
        return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required!", "danger")
            return redirect(url_for("login"))

        # Check if user exists
        user = mongo.db.fusers.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):
            flash("Login successful!", "success")
        else:
            flash("Invalid email or password!", "danger")

        return redirect(url_for("login"))

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
