import re
from flask import Flask, render_template, request, redirect, session
import datetime
import random
import string

import charitycarealgorithm
import createpdf
import getcosts

app = Flask(__name__)
secret_key = ""
for i in range(3):
    secret_key += str(random.randint(0,9))
for i in range(7):
    secret_key += random.choice(string.ascii_letters)
for i in range(2):
    secret_key += str(random.randint(0,9))
app.secret_key = secret_key


def create_pdf_id():
    current_time = str(datetime.datetime.now().strftime("%H_%M_%S"))
    remote_address = str(request.remote_addr.replace(".", "_"))
    random_number = str(random.randint(10000, 99999))
    pdf_id = "{}__{}__{}.pdf".format(current_time, remote_address, random_number)
    return pdf_id

def create_session():
    if 'pdf_id' not in session:
        session['pdf_id'] = create_pdf_id()
    if 'household_size' not in session:
        session['household_size'] = 1
    if 'estimated_annual_income' not in session:
        session['estimated_annual_income'] = 0
    if 'balance_due' not in session:
        session['balance_due'] = 0
    if 'estimated_cost' not in session:
        session['estimated_cost'] = 0

def create_blank_session():
    if 'pdf_id' not in session:
        session['pdf_id'] = create_pdf_id()
    session['household_size'] = 1
    session['estimated_annual_income'] = 0
    session['balance_due'] = 0
    session['estimated_cost'] = 0

def clear_session():
    [session.pop(key) for key in list(session.keys())]
    session.clear()
    create_blank_session()


@app.route("/")
def redirect_to_home():
    return redirect("/home")

@app.route("/home")
def home():
    create_blank_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    return render_template("home.html")

#TODO: create about us page
#TODO: create about charity care page

@app.route("/financiallytest")
def financially_indignant_form():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    return render_template(
        "financially_indignant_form.html",
        household_size = session['household_size'],
        estimated_annual_income = session['estimated_annual_income']
    )

@app.route("/financiallyresult", methods = ["POST", "GET"])
def financially_indignant_result():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    if request.method == "POST":
        session['household_size'] = household_size = int(request.form["household_size"])
        session['estimated_annual_income'] = estimated_annual_income = int(request.form["estimated_annual_income"])
        if charitycarealgorithm.determine_financially_indignant(household_size, estimated_annual_income) != 0:
            return render_template(
                "qualify_success_results.html",
                qualification_type = "Financially",
                pct_discount=100
            )
        else:
            return redirect("/medicallytest")
    else:
        return redirect("/home")

@app.route("/locationsearch")
def select_location():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    return render_template(
        "location_search.html"
    )

@app.route("/chargemaster", methods = ["POST", "GET"])
def select_procedure():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    if request.method == "GET":
        return redirect("/locationsearch")
    location = request.form["facility"]
    return render_template(
        "chargemaster.html",
        procedures = getcosts.get_chargemaster(location)
    )

@app.route("/revealcost", methods = ["POST", "GET"])
def reveal_cost():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    if request.method == "GET":
        return redirect("/locationsearch")
    session['estimated_cost'] = int(float(request.form["cost"]))
    return render_template(
        "reveal_cost.html",
        cost = session['estimated_cost']
    )

@app.route("/medicallytest", methods=["POST", "GET"])
def medically_indignant_form():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    if session['estimated_cost'] != 0:
        return render_template(
            "medically_indignant_form.html",
            household_size = session['household_size'],
            estimated_annual_income = session['estimated_annual_income'],
            balance_due = session['estimated_cost'],
            is_estimate = " (Estimate)"
        )
    else:
        return render_template(
            "medically_indignant_form.html",
            household_size = session['household_size'],
            estimated_annual_income = session['estimated_annual_income'],
            balance_due = session['estimated_cost'],
            is_estimate = " (Estimate)"
    )

@app.route("/medicallyresult", methods = ["POST", "GET"])
def medically_indignant_result():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    if request.method == "POST":
        session['household_size'] = household_size = int(request.form["household_size"])
        session['estimated_annual_income'] = estimated_annual_income = int(request.form["estimated_annual_income"])
        session['balance_due'] = balance_due = int(request.form["balance_due"])
        if charitycarealgorithm.determine_financially_indignant(household_size, estimated_annual_income) != 0:
            return render_template(
                "qualify_success_results.html",
                qualification_type = "Financially",
                pct_discount=100
            )
        if charitycarealgorithm.determine_medically_indignant(household_size, estimated_annual_income, balance_due) != 0:
            if charitycarealgorithm.determine_catastrophic_medically_indignant(household_size, estimated_annual_income, balance_due) != 0:
                return render_template(
                    "qualify_success_results.html",
                    qualification_type = "Catastrophic Medically",
                    pct_discount=100*charitycarealgorithm.determine_catastrophic_medically_indignant(household_size, estimated_annual_income, balance_due)
                )
            return render_template(
                    "qualify_success_results.html",
                    qualification_type = "Medically",
                    pct_discount=100*charitycarealgorithm.determine_medically_indignant(household_size, estimated_annual_income, balance_due)
                )
        elif charitycarealgorithm.determine_tier2_medically_indignant(household_size, estimated_annual_income, balance_due) != 0:
            return render_template(
                    "qualify_success_results.html",
                    qualification_type = "Tier 2 Medically",
                    pct_discount=100*charitycarealgorithm.determine_tier2_medically_indignant(household_size, estimated_annual_income, balance_due)
                )
        elif charitycarealgorithm.determine_catastrophic_medically_indignant(household_size, estimated_annual_income, balance_due) != 0:
            return render_template(
                "qualify_success_results.html",
                qualification_type = "Catastrophic Medically",
                pct_discount=100*charitycarealgorithm.determine_catastrophic_medically_indignant(household_size, estimated_annual_income, balance_due)
            )
        else:
            return render_template("qualify_failure_results.html")
    else:
        return redirect("/home")

@app.route("/blankapplication")
def blank_application():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    return render_template("blank_application.html")

@app.route("/blankapplicationTHP")
def blank_application_THP():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    return render_template("blank_application_THP.html")

@app.route("/blankapplicationUSMDA")
def blank_application_USMDA():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    return render_template("blank_application_USMDA.html")

@app.route("/completeapplication")
def complete_application():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    return render_template("application_completer.html")

@app.route("/completedapplication", methods = ["POST", "GET"])
def display_completed_application():
    create_session()
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    if request.method == "POST":
        application_data = {}
        for key, value in request.form.items():
            application_data[key] = str(value)
        if application_data["facility"] == "USMD Hospital at Arlington":
            createpdf.fill_out_USMDAcharitycare_application(
                "static/" + session["pdf_id"], application_data["curr_date"], application_data["guarantor_name"],
                application_data["last_name"], application_data["first_name"], application_data["MI"], application_data["DOS"],
                application_data["hospital_acct"], application_data['medical_rcrd'], application_data['social_security'],
                application_data["DOB"], application_data['marital_status'], application_data['minors'],
                application_data["living_with"], application_data['legal_minor'], application_data['patient_employed'],
                application_data["spouse_employed"], application_data['med_insurance'], application_data['disability'],
                application_data["disability_length"], application_data['veteran'], application_data['spouse_name'],
                application_data["child1_name"], application_data['child1_age'], application_data['child2_name'],
                application_data["child2_age"], application_data['child3_name'], application_data['child3_age'],
                application_data["child4_name"], application_data['child4_age'], application_data['patient_gross'],
                application_data["patient_net"], application_data['spouse_gross'], application_data['spouse_net'],
                application_data["dependants_gross"], application_data['dependants_net'], application_data['pub_asst_gross'],
                application_data["pub_asst_net"], application_data['food_stamps_gross'], application_data['food_stamps_net'],
                application_data["soc_serc_gross"], application_data['soc_serc_net'], application_data['unemp_gross'],
                application_data["unemp_net"], application_data['strk_ben_gross'], application_data['strk_ben_net'],
                application_data["work_comp_gross"], application_data['work_comp_net'], application_data['alim_gross'],
                application_data["alim_net"], application_data['chld_sup_gross'], application_data['chld_sup_net'],
                application_data["mil_all_gross"], application_data['mil_all_net'], application_data['pen_gross'],
                application_data["pen_net"], application_data['inc_gross'], application_data['inc_net'],
                application_data["rent"], application_data['utilities'], application_data['car'], application_data['groceries'],
                application_data["credit"], application_data['other_descr'], application_data['other'],
                application_data["checking"], application_data['saving'], application_data['CDs_IRAs'],
                application_data["other_invst"], application_data["properties"], application_data["employer_name"],
                application_data["spouse_employer_name"], application_data["employer_phone"],
                application_data["spouse_employer_phone"], application_data['employer_address'],
                application_data["spouse_employer_address"], application_data["occupation"],
                application_data["spouse_occupation"], application_data["medicaid"], application_data["county"],
                application_data["donate"], application_data["liability"], application_data["assist"],
                application_data["assist_identity"], application_data["assist_amnt"], application_data["other_info"],
                application_data["lost_earnings"], application_data["lost_time"]
            )
        elif (
            application_data["facility"] == "Texas Health Center for Diagnostics & Surgery Plano"
            or application_data["facility"] == "Texas Health Harris Methodist Southlake"
            or application_data["facility"] == "Texas Health Presbyterian Hospital Flower Mound"
            or application_data["facility"] == "Texas Health Presbyterian Hospital Rockwall"
            or application_data["facility"] == "Texas Institute for Surgery at Texas Health Presbyterian Dallas"
        ):
            createpdf.fill_out_THP_application(
                "static/" + session["pdf_id"], application_data["curr_date"], application_data["guarantor_name"],
                application_data["last_name"], application_data["first_name"], application_data["MI"], application_data["DOS"],
                application_data["hospital_acct"], application_data['medical_rcrd'], application_data['facility'], application_data['social_security'],
                application_data["DOB"], application_data['marital_status'], application_data['minors'],
                application_data["living_with"], application_data['legal_minor'], application_data['patient_employed'],
                application_data["spouse_employed"], application_data['med_insurance'], application_data['disability'],
                application_data["disability_length"], application_data['veteran'], application_data['spouse_name'],
                application_data["child1_name"], application_data['child1_age'], application_data['child2_name'],
                application_data["child2_age"], application_data['child3_name'], application_data['child3_age'],
                application_data["child4_name"], application_data['child4_age'], application_data['patient_gross'],
                application_data["patient_net"], application_data['spouse_gross'], application_data['spouse_net'],
                application_data["dependants_gross"], application_data['dependants_net'], application_data['pub_asst_gross'],
                application_data["pub_asst_net"], application_data['food_stamps_gross'], application_data['food_stamps_net'],
                application_data["soc_serc_gross"], application_data['soc_serc_net'], application_data['unemp_gross'],
                application_data["unemp_net"], application_data['strk_ben_gross'], application_data['strk_ben_net'],
                application_data["work_comp_gross"], application_data['work_comp_net'], application_data['alim_gross'],
                application_data["alim_net"], application_data['chld_sup_gross'], application_data['chld_sup_net'],
                application_data["mil_all_gross"], application_data['mil_all_net'], application_data['pen_gross'],
                application_data["pen_net"], application_data['inc_gross'], application_data['inc_net'],
                application_data["rent"], application_data['utilities'], application_data['car'], application_data['groceries'],
                application_data["credit"], application_data['other_descr'], application_data['other'],
                application_data["checking"], application_data['saving'], application_data['CDs_IRAs'],
                application_data["other_invst"], application_data["properties"], application_data["employer_name"],
                application_data["spouse_employer_name"], application_data["employer_phone"],
                application_data["spouse_employer_phone"], application_data['employer_address'],
                application_data["spouse_employer_address"], application_data["occupation"],
                application_data["spouse_occupation"], application_data["medicaid"], application_data["county"],
                application_data["donate"], application_data["liability"], application_data["assist"],
                application_data["assist_identity"], application_data["assist_amnt"], application_data["other_info"],
                application_data["lost_earnings"], application_data["lost_time"]
            )
        else:
            createpdf.fill_out_charitycare_application(
                "static/" + session["pdf_id"], application_data["curr_date"], application_data["guarantor_name"],
                application_data["last_name"], application_data["first_name"], application_data["MI"], application_data["DOS"],
                application_data["hospital_acct"], application_data['medical_rcrd'], application_data['facility'], application_data['social_security'],
                application_data["DOB"], application_data['marital_status'], application_data['minors'],
                application_data["living_with"], application_data['legal_minor'], application_data['patient_employed'],
                application_data["spouse_employed"], application_data['med_insurance'], application_data['disability'],
                application_data["disability_length"], application_data['veteran'], application_data['spouse_name'],
                application_data["child1_name"], application_data['child1_age'], application_data['child2_name'],
                application_data["child2_age"], application_data['child3_name'], application_data['child3_age'],
                application_data["child4_name"], application_data['child4_age'], application_data['patient_gross'],
                application_data["patient_net"], application_data['spouse_gross'], application_data['spouse_net'],
                application_data["dependants_gross"], application_data['dependants_net'], application_data['pub_asst_gross'],
                application_data["pub_asst_net"], application_data['food_stamps_gross'], application_data['food_stamps_net'],
                application_data["soc_serc_gross"], application_data['soc_serc_net'], application_data['unemp_gross'],
                application_data["unemp_net"], application_data['strk_ben_gross'], application_data['strk_ben_net'],
                application_data["work_comp_gross"], application_data['work_comp_net'], application_data['alim_gross'],
                application_data["alim_net"], application_data['chld_sup_gross'], application_data['chld_sup_net'],
                application_data["mil_all_gross"], application_data['mil_all_net'], application_data['pen_gross'],
                application_data["pen_net"], application_data['inc_gross'], application_data['inc_net'],
                application_data["rent"], application_data['utilities'], application_data['car'], application_data['groceries'],
                application_data["credit"], application_data['other_descr'], application_data['other'],
                application_data["checking"], application_data['saving'], application_data['CDs_IRAs'],
                application_data["other_invst"], application_data["properties"], application_data["employer_name"],
                application_data["spouse_employer_name"], application_data["employer_phone"],
                application_data["spouse_employer_phone"], application_data['employer_address'],
                application_data["spouse_employer_address"], application_data["occupation"],
                application_data["spouse_occupation"], application_data["medicaid"], application_data["county"],
                application_data["donate"], application_data["liability"], application_data["assist"],
                application_data["assist_identity"], application_data["assist_amnt"], application_data["other_info"],
                application_data["lost_earnings"], application_data["lost_time"]
            )
        return render_template(
            "completed_application.html",
            pdf_src = session['pdf_id']
        )
    else:
        return redirect("/home")

@app.route("/finished")
def final_page():
    createpdf.delete_file("static/{}".format(session['pdf_id']))
    clear_session()
    return render_template("finished.html")