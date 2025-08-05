from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os

# Initialize the Flask application
app = Flask(__name__, static_folder='.', static_url_path='')

# --- IN-MEMORY DATABASE ---
# In a real-world application, you would use a proper database like PostgreSQL,
# MySQL, or a NoSQL database like MongoDB. This list is a simple placeholder
# that will reset every time the server restarts.
applicants_db = []
applicant_id_counter = 1

# --- API ROUTES ---

@app.route('/api/register', methods=['POST'])
def register_applicant():
    """
    Handles new applicant registrations.
    Expects a JSON payload with applicant details.
    """
    global applicant_id_counter
    data = request.get_json()

    # Basic validation
    if not data or not data.get('fullName') or not data.get('email') or not data.get('position'):
        return jsonify({"error": "Missing required fields"}), 400

    new_applicant = {
        "id": applicant_id_counter,
        "fullName": data.get('fullName'),
        "email": data.get('email'),
        "phone": data.get('phone', ''), # Optional field
        "position": data.get('position'),
        "interest": data.get('interest', ''), # Optional field
        "submittedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Add to our "database"
    applicants_db.append(new_applicant)
    applicant_id_counter += 1
    
    # In a real app, you would save to the database here.
    # For example, with SQLAlchemy:
    # db_entry = ApplicantModel(**new_applicant)
    # db.session.add(db_entry)
    # db.session.commit()

    print(f"New applicant registered: {new_applicant['fullName']}")
    return jsonify({"message": "Application received successfully!", "applicant_id": new_applicant['id']}), 201

@app.route('/api/applicants', methods=['GET'])
def get_applicants():
    """
    Returns the list of all applicants.
    """
    # In a real app, you would query the database here.
    # all_applicants = ApplicantModel.query.all()
    # return jsonify([applicant.to_dict() for applicant in all_applicants])
    
    print(f"Retrieved {len(applicants_db)} applicants.")
    return jsonify(applicants_db)

# --- SERVE FRONTEND ---

@app.route('/')
def serve_index():
    """
    Serves the main index.html file.
    """
    # This assumes your index.html is in the same directory as app.py
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """
    Serves other static files if needed (e.g., CSS, JS files).
    This is a fallback for the main static_folder configuration.
    """
    return send_from_directory('.', path)


# --- MAIN EXECUTION ---

if __name__ == '__main__':
    # Running in debug mode is convenient for development.
    # For production, use a proper WSGI server like Gunicorn or uWSGI.
    app.run(debug=True, port=5000)
