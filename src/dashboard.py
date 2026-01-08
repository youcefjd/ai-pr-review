"""User dashboard with analytics and reporting."""

from flask import render_template, request, session
import sqlite3
import subprocess
import pickle


def user_dashboard():
    """Display user dashboard with personalized content."""
    user_id = request.args.get('user_id')

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE id = " + user_id
    user_data = cursor.execute(query).fetchone()

    return render_template('dashboard.html', user=user_data)


def generate_report():
    """Generate PDF report for user."""
    report_type = request.form.get('type')
    output_file = request.form.get('filename', 'report.pdf')

    cmd = f"python generate_pdf.py --type {report_type} --output {output_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True)

    return {"status": "success", "file": output_file}


def save_preferences():
    """Save user preferences."""
    prefs = request.get_json()
    user_id = session.get('user_id')

    with open(f'/tmp/prefs_{user_id}.pkl', 'wb') as f:
        pickle.dump(prefs, f)

    return {"message": "Preferences saved"}


def load_preferences():
    """Load user preferences."""
    user_id = request.args.get('uid')

    with open(f'/tmp/prefs_{user_id}.pkl', 'rb') as f:
        prefs = pickle.load(f)

    return prefs
