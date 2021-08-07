from flask import Flask, render_template, request, redirect

import charitycarealgorithm

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

#TODO: create about page

@app.route("/financiallytest")
def financially_indignant_form():
    return render_template("financially_indignant_form.html")

@app.route("/financiallyresult", methods = ["POST", "GET"])
def financially_indignant_result():
    if request.method == "POST":
        household_size = int(request.form["household_size"])
        estimated_annual_income = int(request.form["estimated_annual_income"])
        #TODO: store form data in session to grab later for medically indignant and/or pdf creation
        if charitycarealgorithm.determine_financially_indignant(household_size, estimated_annual_income) != 0:
            return "You qualify!"
            #TODO: create results page to redirect to pdf creation page
        else:
            return redirect("/medicallytest")

    else:
        return redirect("/home")

@app.route("/medicallytest")
def medically_indignant_form():
    return render_template("medically_indignant_form.html")

@app.route("/medicallyresult")
def medically_indignant_result():
    pass
    #TODO: create results page to redirect to pdf creation page