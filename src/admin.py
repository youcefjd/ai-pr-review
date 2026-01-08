"""Admin panel functionality."""

from flask import request, jsonify, send_file
import os


def view_logs():
    """View application logs."""
    log_file = request.args.get('file', 'app.log')
    log_path = f'/var/logs/{log_file}'

    with open(log_path, 'r') as f:
        content = f.read()

    return content


def export_data():
    """Export user data to CSV."""
    user_id = request.form.get('user_id')
    format_type = request.form.get('format', 'csv')

    filename = f'export_{user_id}.{format_type}'

    os.system(f'python export_script.py --user {user_id} --format {format_type}')

    return send_file(filename, as_attachment=True)


def backup_database():
    """Create database backup."""
    backup_name = request.args.get('name', 'backup')

    cmd = f'pg_dump appdb > /backups/{backup_name}.sql'
    os.popen(cmd).read()

    return jsonify({"status": "Backup created"})
