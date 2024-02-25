from flask import Flask,render_template, request, Response, redirect,flash,request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import test_model
import pandas as pd
import numpy as np
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from werkzeug.utils import secure_filename
import io
import os


#                   DISEASE PREDICTION PAGE

model=test_model.model()
lst=['itching', 'skin_rash', 'nodal_skin_eruptions',
       'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
       'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting',
       'vomiting', 'burning_micturition', 'spotting_ urination',
       'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets',
       'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
       'patches_in_throat', 'irregular_sugar_level', 'cough',
       'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
       'dehydration', 'indigestion', 'headache', 'yellowish_skin',
       'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
       'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea',
       'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
       'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
       'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
       'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure',
       'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
       'fast_heart_rate', 'pain_during_bowel_movements',
       'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus',
       'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity',
       'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes',
       'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties',
       'excessive_hunger', 'extra_marital_contacts',
       'drying_and_tingling_lips', 'slurred_speech', 'knee_pain',
       'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
       'swelling_joints', 'movement_stiffness', 'spinning_movements',
       'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side',
       'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
       'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
       'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain',
       'altered_sensorium', 'red_spots_over_body', 'belly_pain',
       'abnormal_menstruation', 'dischromic _patches',
       'watering_from_eyes', 'increased_appetite', 'polyuria',
       'family_history', 'mucoid_sputum', 'rusty_sputum',
       'lack_of_concentration', 'visual_disturbances',
       'receiving_blood_transfusion', 'receiving_unsterile_injections',
       'coma', 'stomach_bleeding', 'distention_of_abdomen',
       'history_of_alcohol_consumption', 'fluid_overload.1',
       'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations',
       'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
       'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails',
       'inflammatory_nails', 'blister', 'red_sore_around_nose',
       'yellow_crust_ooze']

db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

@app.route("/")
def Disease():
    return render_template('disease.html',lst=lst,pred='',precaution='',desp='',test='',med='',dosage='')

@app.route("/form",methods=['GET', 'POST'])
def form():
    if request.method=='POST':
        Sym1=request.form['Sym1']
        Sym2=request.form['Sym2']
        Sym3=request.form['Sym3']
        Sym4=request.form['Sym4']
        Sym5=request.form['Sym5']
        Sym6=request.form['Sym6']
        lst2=np.zeros((1,len(lst)))
        for i in range(len(lst)):
            if Sym1==lst[i]:
                lst2[0][i]=1.
            elif Sym2==lst[i]:
                lst2[0][i]=1.
            elif Sym3==lst[i]:
                lst2[0][i]=1.
            elif Sym4==lst[i]:
                lst2[0][i]=1.
            elif Sym5==lst[i]:
                lst2[0][i]=1.
            elif Sym6==lst[i]:
                lst2[0][i]=1.
        (pred,flag)=test_model.pred(model,lst2)
        
        if flag:
            precaution=test_model.precaution(pred)
            desp=test_model.description(pred)
        else:
            precaution=''
            desp=''
        lst3=[Sym1,Sym2,Sym3,Sym4,Sym5,Sym6]
        count=lst3.count("Open this select menu")
        while count:
            count-=1
            lst3.remove("Open this select menu")
        (test,med,dosage,s_med,s_dosage)=test_model.medicine(pred,lst3)
        return render_template('disease.html',lst=lst,pred=pred,precaution=precaution,desp=desp,test=test,med=med,dosage=dosage,s_med=s_med,s_dosage=s_dosage,lst3=lst3)
 

#               USER ACCOUNT CREATION

@app.route("/user_account")
def user_account():
    return render_template('account.html')

@app.route("/user_login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        if bool(user.query.filter_by(email_id=email).first()):
            todo=user.query.filter_by(email_id=email).first()
            test=test_report.query.filter_by(num=todo.sno).all()
            return render_template('profile.html',todo=todo,test=test)
        else:
            return render_template("create.html")

@app.route("/create", methods=['GET','POST'])
def create():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        ph_num=request.form['ph_num']
        aadhar=request.form['aadhar']
        date=request.form['date']
        grp=request.form['grp']
        weight=request.form['weight']
        height=request.form['height']
        todo=user(name=name,email_id=email,phone_number=ph_num,aadhar=aadhar,birth_date=date,blood_grp=grp,weight=weight,height=height)
        db.session.add(todo)
        db.session.commit()
        return redirect('/user_account')
    
                    # GRAPH PART

@app.route("/add_bp/<int:sno>", methods=['GET','POST'])
def add_bp(sno):
    if request.method=='POST':
        todo=user.query.filter_by(sno=sno).first()
        test=test_report.query.filter_by(num=todo.sno).all()
        temp=json.loads(todo.blood_press)
        up=request.form['up']
        low=request.form['low']
        temp[str(datetime.utcnow())[:-7]]=[up,low]
        todo.blood_press=json.dumps(temp)
        db.session.commit()
        return render_template('profile.html',todo=todo,test=test)

@app.route("/add_sugar/<int:sno>", methods=['GET','POST'])
def add_sugar(sno):
    if request.method=='POST':
        todo=user.query.filter_by(sno=sno).first()
        test=test_report.query.filter_by(num=todo.sno).all()
        temp=json.loads(todo.Sugar_lev)
        up=request.form['up']
        low=request.form['low']
        temp[str(datetime.utcnow())[:-7]]=[up,low]
        todo.Sugar_lev=json.dumps(temp)
        db.session.commit()
        return render_template('profile.html',todo=todo,test=test)

@app.route("/edit/<int:sno>", methods=['GET','POST'])
def edit(sno):
    if request.method=='POST':
        todo=user.query.filter_by(sno=sno).first()
        test=test_report.query.filter_by(num=todo.sno).all()

    

@app.route('/press_plot/<int:sno>')
def press_plot(sno):
    todo=user.query.filter_by(sno=sno).first()
    temp=json.loads(todo.blood_press)
    fig = test_model.create_figure(temp,"blood_press")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/sugar_plot/<int:sno>')
def sugar_plot(sno):
    todo=user.query.filter_by(sno=sno).first()
    temp=json.loads(todo.Sugar_lev)
    fig = test_model.create_figure(temp,"blood_press")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

#                   UPLOAD AND DOWLOAD PART

ALLOWED_EXTENSIONS=['pdf']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<int:sno>', methods=['GET','POST'])
def upload_file(sno):
    if request.method == 'POST':
        todo=user.query.filter_by(sno=sno).first()
        test=test_report.query.filter_by(num=todo.sno).all()
        role=request.form['role']
        # check if the post request has the file part
        if 'file1' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file1']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path="D:\\Directrix2\\test_Report\\"
            old=os.path.join(path, filename)
            name=role+"-"+str(todo.sno)+'.pdf'
            new=os.path.join(path, name)
            file.save(old)
            os.rename(old,new)
            test=test_report(num=todo.sno,name=role,path=new)
            db.session.add(test)
            db.session.commit()
            return render_template('profile.html',todo=todo,test=test)
    return render_template('profile.html',todo=todo,test=test)

@app.route('/download/<int:sno>')
def routine_show(sno):
    test=test_report.query.filter_by(sno=sno).first()
    path = test.path
    return send_file(path, as_attachment=True)




#                   USER  ACCOUNT DATABASE
class user(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email_id=db.Column(db.String(200),unique=True,nullable=False)
    birth_date=db.Column(db.Integer,default=datetime.utcnow,nullable=False)
    phone_number=db.Column(db.Integer,nullable=False)
    aadhar=db.Column(db.Integer,nullable=False)
    blood_grp=db.Column(db.String(3),nullable=False)
    weight=db.Column(db.Integer,default=0,nullable=True)
    height=db.Column(db.Integer,default=0,nullable=True)
    blood_press=db.Column(db.JSON,default=json.dumps({}, cls=json.JSONEncoder),nullable=True)
    Sugar_lev=db.Column(db.JSON,default=json.dumps({}, cls=json.JSONEncoder), nullable=True)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

class test_report(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    num=db.Column(db.Integer,nullable=False)
    name=db.Column(db.String(200),nullable=False)
    path=db.Column(db.String(1000),nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.num}"


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True,port=8080)