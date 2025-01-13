from flask import Flask, jsonify, request, render_template
import json
import os
from threading import Lock
from uuid import uuid4
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# File path to store bookings
BOOKINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), "bookings.json")

# Ensure the JSON file exists or create it
if not os.path.exists(BOOKINGS_FILE_PATH):
    with open(BOOKINGS_FILE_PATH, 'w') as f:
        json.dump([], f)

# Initialize lock
file_lock = Lock()

# Home endpoint to confirm server is running
@app.route("/")
def home():
    return "Flask App is Running", 200

# Get all bookings
@app.route("/api/bookings", methods=["GET"])
def get_all_bookings():
    try:
        with open(BOOKINGS_FILE_PATH, 'r') as f:
            bookings = json.load(f)
    except Exception as e:
        return jsonify({"error": "Error reading JSON file", "details": str(e)}), 500

    return jsonify(bookings), 200

@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.form

    required_fields = ["first_name", "last_name", "phone_no", "booking_date", "exit_date", "booking_size", "destination", "hotel", "guide"]
    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Parse and validate date fields
        booking_date = datetime.strptime(data["booking_date"], "%Y-%m-%d")
        exit_date = datetime.strptime(data["exit_date"], "%Y-%m-%d")
        current_year = datetime.now().year
        if booking_date.year != current_year or exit_date.year != current_year:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid date format or not within the current year"}), 400

    # Validate phone number
    if not data["phone_no"].isdigit() or not (10 <= len(data["phone_no"]) <= 15):
        return jsonify({"error": "Invalid phone number"}), 400

    # Validate booking size
    try:
        booking_size = int(data["booking_size"])
        if booking_size <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid booking size"}), 400

    # Generate unique ID
    booking_id = str(uuid4())

    new_booking = {
        "booking_id": booking_id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "phone_no": data["phone_no"],
        "booking_date": str(booking_date),
        "exit_date": str(exit_date),
        "booking_size": booking_size,
        "destination": data["destination"],
        "hotel": data["hotel"],
        "guide": True if "guide" in data else False,
    }

    # Acquire lock
    with file_lock:
        try:
            with open(BOOKINGS_FILE_PATH, 'r') as f:
                bookings = json.load(f)
            bookings.append(new_booking)
            with open(BOOKINGS_FILE_PATH, 'w') as f:
                json.dump(bookings, f, indent=2)
        except Exception as e:
            return jsonify({"error": "Error saving booking", "details": str(e)}), 500

    return jsonify(new_booking), 201

# Custom 404 error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Serve the HTML form
@app.route("/add_booking", methods=["GET"])
def add_booking_form():
    current_year = datetime.now().year
    return render_template("add_booking.html", current_year=current_year)

if __name__ == "__main__":
    app.run(debug=True)
