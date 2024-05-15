from flask import Flask, request, redirect, make_response, render_template
import hashlib

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

FLAG = "elio{n0t_4_v3ry_s3cur3_s3ss10n}"

users = {"admin": "mysupersecurepasswordthatnobodycanguess91y2349873rtgsidufhas987rtb"} # ok very cool we dont need persistence

@app.route("/")
def index():
    if "login" in request.cookies:
        return redirect("home")
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if username in users and users[username] == password:
        resp = make_response(redirect("home"))
        resp.set_cookie("login", hashlib.sha1(username.encode()).hexdigest()) # very very secure
        return resp
    return "Login failed!"

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    if not username in users:
        users[username] = password
        resp = make_response(redirect("home"))
        resp.set_cookie("login", hashlib.sha1(username.encode()).hexdigest()) # very very secure
        return resp
    return "Username already exists!"

@app.route("/home")
def home():
    login_cookie = request.cookies.get("login")
    for user in users: # super efficient
        if hashlib.sha1(user.encode()).hexdigest() == login_cookie:
            if user == "admin":
                return f"Hello, admin. The flag is: {FLAG}"
            return f"You are logged in as: {user}. You are not admin, so I cannot give you the flag. :("
    return redirect("/")

if __name__ == "__main__":
    app.run()