from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import re
from datetime import datetime, date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    email = db.Column(db.String(100))
    glucose = db.Column(db.Float)
    haemoglobin = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    remarks = db.Column(db.String(200))

with app.app_context():
    db.create_all()

def predict_health(glucose, haemoglobin, cholesterol):

    if glucose > 126 and cholesterol > 200:
        return "High Risk of Diabetes"

    elif haemoglobin < 12:
        return "Possible Anemia"

    elif cholesterol > 240:
        return "High Cholesterol Risk"

    else:
        return "Healthy"
@app.route('/')
def home():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)


@app.route('/add_patient', methods=['GET', 'POST'])
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        fullname = request.form['fullname']
        dob = request.form['dob']
        email = request.form['email']

        # Email Validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, email):
            return "Invalid Email Address"

        # DOB Validation
        if datetime.strptime(dob, "%Y-%m-%d").date() > date.today():
            return "DOB cannot be a future date"

        try:
            glucose = float(request.form['glucose'])
            haemoglobin = float(request.form['haemoglobin'])
            cholesterol = float(request.form['cholesterol'])
        except ValueError:
            return "Blood values must be numeric"

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        patient = Patient(
            fullname=fullname,
            dob=dob,
            email=email,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            remarks=remarks
        )

        db.session.add(patient)
        db.session.commit()

        return redirect('/')

    return render_template('add_patient.html')

    if request.method == 'POST':

     fullname = request.form['fullname']
     dob = request.form['dob']
     email = request.form['email']

    # Email Validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(pattern, email):
     return "Invalid Email Address"

    # DOB Validation
    if datetime.strptime(dob, "%Y-%m-%d").date() > date.today():
        return "DOB cannot be a future date"

    try:
        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])
    except ValueError:
        return "Blood values must be numeric"

    remarks = predict_health(
        glucose,
        haemoglobin,
        cholesterol
    )
    patient = Patient(
            fullname=fullname,
            dob=dob,
            email=email,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            remarks=remarks
        )

    db.session.add(patient)
    db.session.commit()

    return redirect('/')

    return render_template('add_patient.html')
@app.route('/delete/<int:id>')
def delete(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':

        patient.fullname = request.form['fullname']
        patient.dob = request.form['dob']
        patient.email = request.form['email']
        patient.glucose = float(request.form['glucose'])
        patient.haemoglobin = float(request.form['haemoglobin'])
        patient.cholesterol = float(request.form['cholesterol'])

        patient.remarks = predict_health(
            patient.glucose,
            patient.haemoglobin,
            patient.cholesterol
        )

        db.session.commit()

        return redirect('/')

    return render_template(
        'edit_patient.html',
        patient=patient
    )
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
