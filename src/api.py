"""API endpoints - mixed quality code."""

from flask import Flask, request, jsonify
import os

app = Flask(__name__)


def process_upload():
    """Process file upload - SECURITY ISSUES."""
    file = request.files.get('file')
    
    # VULNERABILITY: No file type validation
    # VULNERABILITY: User controls filename directly
    filename = request.form.get('filename', 'upload.txt')
    
    # VULNERABILITY: Path traversal possible
    filepath = f"uploads/{filename}"
    file.save(filepath)
    
    return jsonify({"message": "File uploaded", "path": filepath})


def execute_command():
    """Execute system command - CRITICAL VULNERABILITY."""
    command = request.args.get('cmd')
    
    # CRITICAL: Command injection - directly executing user input
    result = os.system(command)
    
    return jsonify({"result": result})


# ISSUE: Debug mode enabled (should be False in production)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
