from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired , url
from flask_bootstrap import Bootstrap5
import csv
import smtplib
import os
import datetime

EMAIL = os.getenv('email')
PASSWORD = os.getenv('password')
RECEIVER = os.getenv('rec')

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY']=os.getenv('key','thisisnotansecret')

@app.context_processor
def inject_year():
    return {'current_year':datetime.datetime.now().year}

class AddCafe(FlaskForm):
    choice_food = [('🤌'), ('🤌🤌'), ('🤌🤌🤌'), ('🤌🤌🤌🤌'), ('🤌🤌🤌🤌🤌')]
    choice_ambience = [('✨'), ('✨✨'), ('✨✨✨'), ('✨✨✨✨'), ('✨✨✨✨✨')]
    choice_staff = [('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪️'), ('💪💪💪💪💪')]
    choice_bool = ['YES','NO']
    image = StringField("Cafe's Image",validators=[DataRequired(),url()])
    name =  StringField("Cafe's Name",validators=[DataRequired()])
    about = StringField("About Cafe",validators=[DataRequired()])
    food = SelectField("Food",choices=choice_food)
    ambience = SelectField("Ambience",choices=choice_ambience)
    staff = SelectField("Staff",choices=choice_staff)
    wifi = SelectField("WiFi",choices=choice_bool)
    power = SelectField("Power Outlets",choices=choice_bool)
    location = StringField("Location Url",validators=[DataRequired(),url()])
    submit = SubmitField("ADD")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html',cafe=list_of_rows)

@app.route('/contact',methods=["POST"])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    mail_body = f"subject:Message from {name}\n\nEmail: {email}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=RECEIVER, msg=mail_body)
    message = f"{name} Your message has been sent successfully !"
    return render_template("index.html", messages=message)

@app.route('/append_cafes_list',methods=["GET","POST"])
def add():
    form = AddCafe()
    if form.validate_on_submit():
        data = [
            request.form['image'],
            request.form['name'],
            request.form['about'],
            request.form['food'],
            request.form['ambience'],
            request.form['staff'],
            request.form['wifi'],
            request.form['power'],
            request.form['location']
        ]
        row = ','.join(data)
        with open('cafe-data.csv', mode='a', encoding='UTF-8') as csv_file:
            csv_file.write(row + '\n')
            csv_file.flush()
            message = "Cafe added successfully !"
            return render_template('index.html',messages=message)
    return render_template('addcafe.html',form=form)



if __name__ == '__main__':
    app.run(debug=False)