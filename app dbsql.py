from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

db_path = "C:/Semester 2/Week 10/bookings.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Booking Model which I GPT-ed
class Booking(db.Model):
    __tablename__ = "bookings"

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    start_date = db.Column(db.String(10), nullable=True)
    end_date = db.Column(db.String(10), nullable=True)
    no_people = db.Column(db.Integer, nullable=True)
    destination = db.Column(db.String(100), nullable=True)
    hotel = db.Column(db.String(100), nullable=True)

with app.app_context():
    db.create_all()  #The creating of the database in case it doesn't exist


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # the new data 4 booking
        new_booking = Booking(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            phone_no=request.form["phone_no"],
            start_date=request.form["start_date"],
            end_date=request.form["end_date"],
            no_people=request.form["no_people"],
            destination=request.form["destination"],
            hotel=request.form["hotel"],
        )
        db.session.add(new_booking)
        db.session.commit()


        return redirect(url_for("home"))


    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)