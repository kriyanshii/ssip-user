from flask import *
from  base import app
import random
from base.com.Dao.user_feedback_dao import UserFeedbackDao
from base.com.Vo.user_feedback_vo import UserFeedbackVo
from base.com.Dao.police_station_dao import PoliceStationDao
from base.com.Vo.police_station_vo import PoliceStationVo
from twilio.rest import Client

app.config['SECRET_KEY'] = 'inbniotySGjuejwfgGYUYGuwefruhfiUUHUHUguuggukgrekj'

@app.route('/')
def home():

    police_station_dao = PoliceStationDao()
    police_station_vo = PoliceStationVo

    ps_list = police_station_dao.view_ps()
    list1 = []
    uniques = []

    for i in range(len(ps_list)):
        count = list1.count(ps_list[i].district)
        if count==0:
            uniques.append(ps_list[i].district)
            list1.append(ps_list[i].district)

    return render_template("enter_number.html",uniques=uniques)

@app.route('/handle_data',methods=['POST'])
def handle_data():

    p_number = "+91" + request.form['phonenumber']
    val = getOtpApi(p_number)
    district = request.form["district"]
    session['district'] = district

    if val:
        return render_template("enter_otp.html")
    else:
        flash("There was error please try again")
        return render_template("enter_number.html")

@app.route("/validate_otp",methods=["POST"])
def validate_otp():
    otp = request.form['Otp']
    if "response" in session:
        s = session['response']
        session.pop('response',None)
        if s == otp:
            return redirect("/load_police_stations")
        else:
            flash("Authentication not succesful")
            return render_template("enter_number.html")

@app.route('/resendOTP',methods = ['POST'])
def resendOTP():
    return render_template("enter_number.html")

@app.route('/load_police_stations')
def load_police_stations():

    police_station_dao = PoliceStationDao()
    ps_list = police_station_dao.view_ps()
    list1 = []

    for i in range(len(ps_list)):
        if session["district"]==ps_list[i].district:
            list1.append(ps_list[i].police_station_name)

    return render_template("user_form.html",list1=list1)

@app.route('/insert_user_feedback',methods=["POST"])
def insert_user_feedback():

    police_station_name = request.form.get("police_station_name")
    question_1 = request.form.get("question_1")
    question_2 = request.form.get("question_2")
    paragraph = request.form.get("paragraph")

    list1 = paragraph.split(" ")
    if len(list1)>300:
        flash("Limit of 300 words exceeded!!")
        return redirect('/load_police_stations')

    user_feedback_vo = UserFeedbackVo()
    user_feedback_dao = UserFeedbackDao()

    user_feedback_vo.police_station_name = police_station_name
    user_feedback_vo.question_1 = question_1
    user_feedback_vo.question_2 = question_2
    user_feedback_vo.district = session["district"]
    user_feedback_vo.paragraph = paragraph

    user_feedback_dao.insert_feedback(user_feedback_vo)

    return render_template("done.html")


def generateOTP():
    return random.randrange(100000,999999)

def getOtpApi(p_number):
    account_sid = 'AC5b6de0bce3f5033b476efac822d6e4a1'
    auth_token = 'e2f2d212c9dc4a20d6fda1e4e2481817'
    OTP = generateOTP()
    print(OTP)
    body = "Your otp is" + str(OTP)
    session['response'] = str(OTP)
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body = body,
        from_= '+12202205492',
        to=p_number)

    if message.sid:
        return True
    else:
        return False




