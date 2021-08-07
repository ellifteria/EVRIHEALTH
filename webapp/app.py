from flask import Flask, render_template, request, redirect, session
import datetime
import random

import charitycarealgorithm

app = Flask(__name__)
app.secret_key = "98hgjNXB12"

def create_pdf_id():
    current_time = str(datetime.datetime.now().strftime("%H_%M_%S"))
    remote_address = str(request.remote_addr.replace(".", "_"))
    random_number = str(random.randint(1000, 9999))
    pdf_id = "{}__{}__{}.pdf".format(current_time, remote_address, random_number)
    return pdf_id

def create_session():
    if 'pdf_id' not in session:
        create_pdf_id()
    if 'household_size' not in session:
        session['household_size'] = 1
    if 'estimated_annual_income' not in session:
        session['estimated_annual_income'] = 0
    if 'balance_due' not in session:
        session['balance_due'] = 0

def create_blank_session():
    if 'pdf_id' not in session:
        create_pdf_id()
    session['household_size'] = 1
    session['estimated_annual_income'] = 0
    session['balance_due'] = 0


@app.route("/")
def redirect_to_home():
    return redirect("/home")

@app.route("/home")
def home():
    create_blank_session()
    return render_template("home.html")

#TODO: create about us page
#TODO: create about charity care page

@app.route("/financiallytest")
def financially_indignant_form():
    create_session()
    return render_template(
        "financially_indignant_form.html",
        household_size = session['household_size'],
        estimated_annual_income = session['estimated_annual_income']
    )

@app.route("/financiallyresult", methods = ["POST", "GET"])
def financially_indignant_result():
    if request.method == "POST":
        session['household_size'] = household_size = int(request.form["household_size"])
        session['estimated_annual_income'] = estimated_annual_income = int(request.form["estimated_annual_income"])
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
    create_session()
    return render_template(
        "medically_indignant_form.html",
        household_size = session['household_size'],
        estimated_annual_income = session['estimated_annual_income'],
        balance_due = session['balance_due'],
    )

@app.route("/medicallyresult")
def medically_indignant_result():
    if request.method == "POST":
        session['household_size'] = household_size = int(request.form["household_size"])
        session['estimated_annual_income'] = estimated_annual_income = int(request.form["estimated_annual_income"])
        session['balance_due'] = balance_due = int(request.form["balance_due"])
        #TODO: store form data in session to grab later for medically indignant and/or pdf creation
        if charitycarealgorithm.determine_medically_indignant(household_size, estimated_annual_income, balance_due) != 0:
            if charitycarealgorithm.determine_catastrophic_medically_indignant(household_size, estimated_annual_income, balance_due) != 0:
                return "You qualify for catastrophic medically indignant financial assistance!"
                #TODO: create results page to redirect to pdf creation page
            return "You qualify for medically indignant financial assistance!"
            #TODO: create results page to redirect to pdf creation page
        elif charitycarealgorithm.determine_tier2_medically_indignant(household_size, estimated_annual_income, balance_due) != 0:
            return "You qualify for tier 2 medically indignant financial assistance!"
            #TODO: create results page to redirect to pdf creation page
        elif charitycarealgorithm.determine_catastrophic_medically_indignant(household_size, estimated_annual_income, balance_due) != 0:
            return "You qualify for catastrophic medically indignant financial assistance!"
            #TODO: create results page to redirect to pdf creation page
        else:
            return "Sorry, you don't qualify"

    else:
        return redirect("/home")