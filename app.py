import os
from forms import RegisterForm, DeleteForm
from flask import Flask, render_template, url_for, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import videotoimg as vt
import cv2
import faceRecognition as fr
import time
from collections import Counter
#import winsound
import shutil

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Student(db.Model):
    __tablename__='students'
    id=db.Column(db.Integer)
    name=db.Column(db.Text)
    email=db.Column(db.Text)
    roll=db.Column(db.Integer,primary_key=True)
    branch=db.Column(db.Text)
    sec=db.Column(db.Text)
    status=db.Column(db.Integer)
    
    def __init__(self,name,email,roll,branch,sec,status):
        self.name=name
        self.email=email
        self.roll=roll
        self.branch=branch
        self.sec=sec
        self.status=status
    
    def __repr__(self):
        return f"{self.roll}"
        #table

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_student',methods=['GET','POST'])
def add_student():
    form=RegisterForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        roll=form.roll.data
        branch=form.branch.data
        sec=form.sec.data
        status=form.status.data
        new_data=Student(name,email,roll,branch,sec,status)
        db.session.add(new_data)
        db.session.commit() 
        vt.done(roll)
        
        return redirect(url_for('list'))
    
    return render_template('add.html',form=form)

@app.route('/delete',methods=['GET','POST'])
def delete():
    form =DeleteForm()
    if form.validate_on_submit():
        roll=form.roll.data
        student=Student.query.filter_by(roll=roll).first()
        path="/home/siva_ganesh/zips/projects/AttendanceSystem/static/"
        path+=str(student)
        if student:
             shutil.rmtree(path)
             db.session.delete(student)
             db.session.commit()
        else:
            return redirect(url_for('error'))
            
        
        return redirect(url_for('list'))
         
    return render_template('delete.html',form=form)

@app.route('/list')
def list():
    students=Student.query.all()
    
    return render_template('list.html',students=students)

@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/faculty')
def teacher():
    return render_template('teacher.html')

@app.route('/attendance')
def attendance():
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('trainingData.yml')#Load saved training data
    students=Student.query.all()
    name=Counter()
    i=0
    for ele in students:
        ele.status=0
        name[i]=ele
        i+=1
    db.session.commit()
    cap=cv2.VideoCapture(0)
    start=time.time()
    while i and name:
        ret,test_img=cap.read()# captures frame and returns boolean value and captured image
        faces_detected,gray_img=fr.faceDetection(test_img)
    
    
    
        for (x,y,w,h) in faces_detected:
          cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)
    
        resized_img = cv2.resize(test_img, (1000, 700))
        cv2.imshow('face detection Tutorial ',resized_img)
        cv2.waitKey(10)
    
    
        for face in faces_detected:
            (x,y,w,h)=face
            roi_gray=gray_img[y:y+w, x:x+h]
            label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
            print("confidence:"+str(confidence))
            print("label:"+str(label))
            fr.draw_rect(test_img,face)
            a=Student.query.filter_by(roll=label).first()
            if confidence<39 and a.status==0:
                a.status=1
                db.session.commit()
                #winsound.Beep(2500, 1200)
                duration = 1  # seconds
                freq = 440  # Hz
                os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
                i-=1
                fr.put_text(test_img,str(a),x,y) 
        end=time.time()
        if cv2.waitKey(30) & 0xFF ==ord('q'):
            break
        if int(end-start)>=180:
            break
    cap.release()
    cv2.destroyAllWindows()
    
    return redirect(url_for('result'))


@app.route('/result')
def result():
    a=Student.query.filter_by(status=0).all()
    if len(a)==0:
        return redirect(url_for('NoCase'))
    else:
        #return redirect(url_for('Reupdate'))
        return render_template('result.html',li=a)

@app.route('/Reupdate',methods=["POST"])
def Reupdate():
    form_data=request.form
    print(form_data)
    a=form_data['student']
    stud=Student.query.filter_by(roll=int(a)).first()
    stud.status=1
    db.session.commit()
    return redirect("/result")

@app.route('/Display',methods=["POST"])
def Display():
    a=Student.query.filter_by(status=0).all()
    if len(a)==0:
        return redirect('NoCase')
    else:
        return render_template('display.html',li=a)
        
@app.route('/NoCase')
def NoCase():
    return render_template("Nocase.html")

@app.errorhandler(404)
def errorhandler(e):
    return render_template("errorhandler.html")
     
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
        

