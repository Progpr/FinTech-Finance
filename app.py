import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from openai import OpenAI
from datetime import datetime
import requests
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

INCOME = [
    "Less than $10000",
    "$10000-$20000",
    "$20000-$30000",
    "$30000-$40000",
    "$40000-$50000",
    "$50000-$60000",
    "$60000-$70000",
    "$70000-$80000",
    "$80000-$90000",
    "$90000-$100,000",
    "More than $100,000",
]

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    user_id = session["user_id"]
    users = db.execute("select username from users where id = ?",user_id)
    username = users[0]["username"]
    purchases_db = db.execute("select stock, sum(shares) As shares, price from purchases where username = ? Group by stock",username)
    cash_db = db.execute("select cash from users where id = ?",user_id)
    cash = cash_db[0]["cash"]

    gtotal = cash

    for purchase in purchases_db:
        stock = purchase["stock"]
        quote= lookup(stock)
        gtotal += int(purchase["price"]*purchase["shares"])

    return render_template("index.html",purchases_db = purchases_db, username=username, cash = cash, gtotal = gtotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    else:
        userid = session["user_id"]
        usernames = db.execute("select username from users where id = ?",userid)
        username = usernames[0]["username"]
        money = db.execute("select cash from users where username = ?",username)
        cash = int(money[0]["cash"])
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        quote = lookup(str(symbol).upper())

        if not symbol:
            return apology("Please enter a symbol!",403)

        if quote==None:
            return apology("Invalid Symbol!",400)

        if shares < 0:
            return apology("Number of shares cannot be negative",400)

        if type(shares)!=type(3):
            return apology("Invalid number of shares!,400")

        if cash < shares*quote["price"]:
            return apology("Sorry! you don't have enough funds to purchase this stock",403)

        amount = cash - (shares*quote["price"])

        date = datetime.now()
        db.execute("Insert into purchases(username, stock, shares, price, type, DT) values(?,?,?,?,'B',?)",username, quote["name"], shares, quote["price"],date)
        db.execute("Update users set cash = ? where id = ?",amount,userid)

        flash("BOUGHT!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """show history of transactions"""
    purchases_buy = db.execute("select * from purchases where type='B'")
    purchases_sell = db.execute("select * from purchases where type='S'")
    return render_template("history.html", purchases_buy=purchases_buy, purchases_sell=purchases_sell)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/forget", methods=["GET","POST"])
def forget():
    """to change user's password"""
    if request.method=="GET":
        return render_template("forget.html")
    else:
        input_username = request.form.get("username")
        new_password = request.form.get("new_password")
        old_password = request.form.get("old_password")

        users = db.execute("select * from users where username = ?",input_username)

        if len(users) != 1 or not check_password_hash(users[0]["hash"], old_password):
            return apology("invalid username and/or old password", 403)

        if not input_username:
            return apology("Enter you username!",403)

        if not old_password:
            return apology("Retype your old password!",403)

        if not new_password:
            return apology("Make a new password!",403)

        if old_password == new_password:
            return apology("The new password cannot be the same as the old password",403)

        hash_password = generate_password_hash(new_password)
        db.execute("update users set hash = ? where username = ?",hash_password,input_username)

        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    stock = request.form.get("symbol")
    quote = lookup(str(stock).upper())

    if request.method =="GET":
        return render_template("quote.html")

    else: # if user submits by POST

        # to check if field is empty
        if not stock:
            return apology("Symbol field cannot be blank",400)

        # to check if stock symbol is valid
        if quote == None:
            return apology("Invalid Stock Symbol",400)

        # displaying the results
        return render_template("quoted.html", symbol=stock,name=quote["name"],price=quote["price"])



@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    rows = db.execute("Select * From users where username = ?",username)
    Email = request.form.get("email")
    Pan = request.form.get("pan")
    Aadhar = request.form.get("aadhar")
    Gender = request.form.get("gender")
    Phone = request.form.get("phone")
    Bank = request.form.get("bank")
    Income = request.form.get("income")

    if (request.method=="POST"):



        # to check if username exists
        if len(rows)==1:
            return apology("Username already exists",400)

        # to check if passwords match
        if password != confirmation:
            return apology("Passwords do not match!",400)

        # to check for blank fields
        #if not username or not password or not confirmation or not Phone or not Email or not Pan or not Gender or not Aadhar or not Bank or not Income:
            #return apology("Fields are blank, Go back and enter all the details",400)

        password_hash = generate_password_hash(password)
        db.execute("Insert into users(username,hash,Aadhar,Gender,Income,Bank,Pan,Phone,Email) values(?,?,?,?,?,?,?,?,?)",username,password_hash,Aadhar,Gender,Income,Bank,Pan,Phone,Email)

        return redirect("/login")

    else:
        return render_template("register.html",INCOME=INCOME)



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    usernames = db.execute("select username from users where id = ?",user_id)
    username = usernames[0]["username"]

    if request.method == "GET":
        # to eliminate the risk of user selecting a stock that he or she does not have, the select menu
        # will display stocks that the user already owns
        stocks_db = db.execute("select stock from purchases where username = ? group by stock", username)

        return render_template("sell.html",stocks_db = stocks_db)

    else:
        money = db.execute("select cash from users where id = ?",user_id)
        cash = int(money[0]["cash"])
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        quote = lookup(str(symbol).upper())

        if not symbol:
            return apology("Please enter a symbol!",403)

        if quote==None:
            return apology("Invalid Symbol!",403)

        if shares < 0:
            return apology("Number of shares cannot be negative",403)

        if type(shares)!=type(3):
            return apology("Invalid number of shares!,400")

        amount = cash + (shares*quote["price"])

        user_shares = db.execute("select shares from purchases where username = ? and stock = ? group by stock",username,symbol )
        user_share = int(user_shares[0]["shares"])

        if shares > user_share:
            return apology("You do not have that many shares!",403)

        updated_shares = user_share - shares

        date = datetime.now()
        db.execute("Insert into purchases(username, stock, shares, price, type, DT) values(?,?,?,?,'S',?)",username, quote["name"],(-1)*shares, quote["price"],date)
        db.execute("Update users set cash = ? where id = ?",amount,user_id)

        flash("SOLD!")
        return redirect("/")



@app.route("/fundamentals")
def fundamentals():
    return render_template("fundamentals.html")


@app.route("/ask")
def ask():
    return render_template("ask.html")

@app.route("/response", methods=["GET","POST"])
def respose():
    if request.method == ""



    ##openAI logic



     return render_template("response.html")

@app.route("/bot", methods=[""])
def bot():

    return render_template("bot.html")


@app.route("/watchlist")
def watchlist():
    return render_template("watchlist.html")
