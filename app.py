from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy     # type: ignore
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"

db = SQLAlchemy(app)
app.app_context().push()

class Employee(db.Model):						
    sno = db.Column(db.Integer, primary_key = True)			 
    name = db.Column(db.String(200), nullable = False)			
    email = db.Column(db.String(200), nullable = False)		
    contact = db.Column(db.String(12), nullable = True)
    
    def __repr__(self):
         return f"{self.sno}-{self.name}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        name=(request.form['name'])
        email=(request.form['email'])
        contact=(request.form['contact'])
        employee = Employee(name = name, email = email , contact=contact)	
        db.session.add(employee)							
        db.session.commit()		
    allemployee = Employee.query.all()
    return render_template("index.html", allemployee=allemployee)

    # return "<p>Hello, World!</p>"

@app.route("/about")
def about():
    allemployee = Employee.query.all()
    return "<p> this is about page</p>"

@app.route("/display")
def display():
     allemployee= Employee.query.all()
     return"<p> this is display page</p>"

@app.route("/delete/<int:sno>")
def delete(sno):
   employee= Employee.query.filter_by(sno=sno).first()
   db.session.delete(employee)
   db.session.commit()
   return redirect("/")

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
     if request.method=='POST':
        name=(request.form['name'])
        email=(request.form['email'])
        contact=(request.form['contact'])
        employee= Employee.query.filter_by(sno=sno).first()
        employee.name = name
        employee.email = email 
        employee.contact=contact
        db.session.add(employee)
        db.session.commit()
        return redirect("/")
     
     employee= Employee.query.filter_by(sno=sno).first()
     return render_template("update.html", employee = employee)

if __name__=="__main__":
    app.run(debug=True) 