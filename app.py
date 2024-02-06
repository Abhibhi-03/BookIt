from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import current_app, g
import sqlite3
import click
from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, SelectField
import random



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Project1.db'
db = SQLAlchemy(app)

class Venues(db.Model):
   __tablename__="venues"
   id = db.Column(db.Integer, primary_key=True)
   Ven_Name=db.Column(db.String(200))
   Artist_Name=db.Column(db.String(200))
   Ven_descrip=db.Column(db.String(10000))
   Ven_Date=db.Column(db.String)
   Seats_Avail=db.Column(db.Integer)
   Type_Seats=db.Column(db.Integer)
   Type1_Name=db.Column(db.String(200), nullable=False)
   Type2_Name=db.Column(db.String(200))
   Type3_Name=db.Column(db.String(200))
   Type4_Name=db.Column(db.String(200))
   Type1_Price=db.Column(db.Float)
   Type2_Price=db.Column(db.Float)
   Type3_Price=db.Column(db.Float)
   Type4_Price=db.Column(db.Float)
   Type1_Seats=db.Column(db.Integer)
   Type2_Seats=db.Column(db.Integer)
   Type3_Seats=db.Column(db.Integer)
   Type4_Seats=db.Column(db.Integer)
   Balance=db.Column(db.Float)
   
   booked = db.relationship('Ticket', backref='venues', lazy=True)

   def _repr_(self):
        return '<V_ID %r>' % self.id
    
class Ticket(db.Model):
    __tablename__="ticket"
    id = db.Column(db.Integer, primary_key=True)
    concert_id= db.Column(db.Integer,db.ForeignKey('venues.id'))
    ticket_num=db.Column(db.Integer)
    Number_of_Seats=db.Column(db.Integer)
    Type_of_seats=db.Column(db.String(200))
    Name=db.Column(db.String(200))
    Number=db.Column(db.Integer)
    Client_type=db.Column(db.String(200))
        
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
        V_ID = Venues.query.order_by(Venues.Ven_Date).all()
        return render_template('index.html', V_ID=V_ID)
    
@app.route('/Post_ven', methods=['GET','POST'])
def Post_ven():
    if request.method == 'POST':
        Name=request.form['Ven_Name']
        Artist_Name=request.form['Artist_Name']
        Ven_descrip=request.form['Ven_descrip']
        Ven_Date=request.form['Ven_Date']
        Seats_Avail=request.form['Seats_Avail']
        Type_seats=request.form['types']
        Type1_Name=request.form['Type1_Name']
        Type2_Name=request.form['Type2_Name']
        Type3_Name=request.form['Type3_Name']
        Type4_Name=request.form['Type4_Name']
        Type1_Price=request.form['Type1_Price']
        Type2_Price=request.form['Type2_Price']
        Type3_Price=request.form['Type3_Price']
        Type4_Price=request.form['Type4_Price']
        Type1_Seats=request.form['Type1_Seats']
        Type2_Seats=request.form['Type2_Seats']
        Type3_Seats=request.form['Type3_Seats']
        Type4_Seats=request.form['Type4_Seats']
        Balance=request.form['Balance']
        print("this is working")
        percent=request.form['percent']
        if percent=="Yes":
            Seats_Avail=int(Seats_Avail)*0.50


        new_Ven=Venues(Ven_Name=Name,Artist_Name=Artist_Name,Ven_descrip=Ven_descrip,
                       Ven_Date=Ven_Date,Seats_Avail=Seats_Avail,Type_Seats=Type_seats,
                       Type1_Name=Type1_Name,Type2_Name=Type2_Name,Type3_Name=Type3_Name,Type4_Name=Type4_Name,
                       Type1_Price=Type1_Price,Type2_Price=Type2_Price,Type3_Price=Type3_Price,Type4_Price=Type4_Price,
                       Type1_Seats=Type1_Seats,Type2_Seats=Type2_Seats,Type3_Seats=Type3_Seats,Type4_Seats=Type4_Seats,Balance=Balance)
        try:
            db.session.add(new_Ven)
            db.session.commit()
            return redirect('/Post_ven')
        except:
            return 'There was an issue adding your task. You may have left an field empty'
    else :
        V_ID = Venues.query.order_by(Venues.Ven_Date).all()
        return render_template('index.html', V_ID=V_ID)
      


@app.route('/Ven_update', methods=['POST', 'GET'])
def Ven_update():
    if request.method == 'POST':
        return render_template('Ven_update.html')
    else:
        return render_template('index.html')
      

@app.route('/book/<int:id>',methods=['GET','POST'])
def book(id):
    task = Venues.query.get_or_404(id)
    if request.method == 'POST':
        task = Venues.query.get_or_404(id)

    else:
        return render_template('book.html', task=task)



@app.route('/Final_Confirmation/<int:id>',methods=['GET','POST'])
def Final_Confirmation(id):
    task = Venues.query.get_or_404(id)
    if request.method == 'POST':
     Ticket_Num=random.randint(1,1999999)
     Name=request.form['Name']
     Number=request.form['Number']
     Type_Name=request.form['type']
     Client_type=request.form['Client_Type']
     Number_of_Seats=request.form['Number_Seats']
     new_booking=Ticket(Name=Name,Number=Number,concert_id=id,Type_of_seats=Type_Name,Client_type=Client_type,Number_of_Seats=Number_of_Seats,
                        ticket_num=Ticket_Num)
     task.Seats_Avail-=int(Number_of_Seats)
     if Type_Name==task.Type1_Name:
         task.Balance+= (int(Number_of_Seats)*task.Type1_Price)
         task.Type1_Seats-=int(Number_of_Seats)
     elif Type_Name==task.Type2_Name:
         task.Balance+= (int(Number_of_Seats)*task.Type2_Price)
         task.Type2_Seats-=int(Number_of_Seats)
     elif Type_Name==task.Type3_Name:
         task.Balance+= (int(Number_of_Seats)*task.Type3_Price)
         task.Type3_Seats-=int(Number_of_Seats)
     elif Type_Name==task.Type4_Name:
         task.Balance+= (int(Number_of_Seats)*task.Type4_Price)
         task.Type4_Seats-=int(Number_of_Seats)
     try:
       db.session.commit()
     except:
        return 'There was an issue adding your task. You may have left an field empty'
     try:
         db.session.add(new_booking)
         db.session.commit()
         return redirect('/Ticket_Display')

     except:
         return 'There was an issue adding your task. You may have left an field empty'

    else:
        return render_template('index.html')

@app.route('/Ticket_Display',methods=['GET','POST'])
def Ticket_Display():
 if request.method == 'POST':
       V_ID = Venues.query.order_by(Venues.Ven_Date).all()
       return render_template('index.html', V_ID=V_ID)
 else:
       ticket_Id = Ticket.query.order_by(Ticket.id.desc()).first()
       return render_template('Ticket_Display.html', ticket_Id=ticket_Id)
if __name__ == "__main__":
    app.run(debug=True)
