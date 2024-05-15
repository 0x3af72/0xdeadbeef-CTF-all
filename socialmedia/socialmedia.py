from flask import Flask, request, redirect, make_response, render_template
import hashlib
import secrets
import string

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

users = {"admin": "mysupersecurepasswordthatnobodycanguess91y2349873rtgsidufhas987rtb"} # ok very cool we dont need persistence
profiles = {"admin": {"pfp": "https://www.shutterstock.com/image-vector/default-avatar-profile-icon-social-600nw-1677509740.jpg", "description": "MWAHAHAHAHA! Nobody can steal my cookies!"}}
sessions = {"hPJB5P7LGITAwhfsPVO49wOcM8JImIor": "admin"}

def create_session(username):
    session_id = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))
    sessions[session_id] = username
    return session_id

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
        resp.set_cookie("login", create_session(username)) # very very secure
        return resp
    return "Login failed!"

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    if not username in users:
        users[username] = password
        profiles[username] = {"pfp": "https://www.shutterstock.com/image-vector/default-avatar-profile-icon-social-600nw-1677509740.jpg", "description": "No description set."}
        resp = make_response(redirect("home"))
        resp.set_cookie("login", create_session(username)) # very very secure
        return resp
    return "Username already exists!"

@app.route("/home")
def home():
    login_cookie = request.cookies.get("login")
    if login_cookie in sessions:
        if sessions[login_cookie] == "admin":
            return "Congratulations, you won! The flag is: elio{c00k13_st34l1ng_w1th_xss_0x3af72}"
        return render_template("home.html", username=sessions[login_cookie])
    resp = make_response(redirect("/"))
    resp.set_cookie("login", "", expires=0)
    return resp

@app.route("/profile/<username>")
def profile(username):
    login_cookie = request.cookies.get("login")
    if not login_cookie in sessions:
        resp = make_response(redirect("/"))
        resp.set_cookie("login", "", expires=0)
        return resp
    isuser = False
    if username == sessions[login_cookie]:
        isuser = True
    if username in users:
        return render_template("profile.html", username=username, pfp=profiles[username]["pfp"], description=profiles[username]["description"], isuser=isuser)
    return "User does not exist!"

@app.route("/update_description", methods=["POST"])
def update_description():
    login_cookie = request.cookies.get("login")
    if not login_cookie in sessions:
        resp = make_response(redirect("/"))
        resp.set_cookie("login", "", expires=0)
        return resp
    if sessions[login_cookie] == "admin":
        return "Congratulations, you won! The flag is: elio{c00k13_st34l1ng_w1th_xss_0x3af72}"
    username = request.form["username"]
    description = request.form["description"]
    if not username == sessions[login_cookie]:
        return redirect("/home")
    profiles[username]["description"] = description
    return redirect(f"/profile/{username}")

@app.route("/update_pfp", methods=["POST"])
def update_pfp():
    login_cookie = request.cookies.get("login")
    if not login_cookie in sessions:
        resp = make_response(redirect("/"))
        resp.set_cookie("login", "", expires=0)
        return resp
    if sessions[login_cookie] == "admin":
        return "Congratulations, you won! The flag is: elio{c00k13_st34l1ng_w1th_xss_0x3af72}"
    username = request.form["username"]
    description = request.form["pfp"]
    if not username == sessions[login_cookie]:
        return redirect("/home")
    profiles[username]["pfp"] = description
    return redirect(f"/profile/{username}")

@app.route("/report")
def report():
    login_cookie = request.cookies.get("login")
    if not login_cookie in sessions:
        resp = make_response(redirect("/"))
        resp.set_cookie("login", "", expires=0)
        return resp
    if sessions[login_cookie] == "admin":
        return "Congratulations, you won! The flag is: elio{c00k13_st34l1ng_w1th_xss_0x3af72}"
    return render_template("report.html")

import time # idc
def view_report(reported_user): # bot that gets xssed
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    try:
        driver.get("http://localhost:5000")
        driver.add_cookie({"name": "login", "value": "hPJB5P7LGITAwhfsPVO49wOcM8JImIor"})
        driver.get(f"http://localhost:5000/profile/{reported_user}")
        time.sleep(2)
    finally:
        driver.quit()
        return True

@app.route("/send_report", methods=["POST"])
def send_report():
    login_cookie = request.cookies.get("login")
    if not login_cookie in sessions:
        resp = make_response(redirect("/"))
        resp.set_cookie("login", "", expires=0)
        return resp
    if sessions[login_cookie] == "admin":
        return "Congratulations, you won! The flag is: elio{c00k13_st34l1ng_w1th_xss_0x3af72}"
    reported_user = request.form.get("reported_user")
    if reported_user in users:
        if view_report(reported_user):
            return "Report has been reviewed by the admin!"
        return "Something went wrong... contact the trainers"
    return "This user does not exist!"

if __name__ == "__main__":
    app.run()