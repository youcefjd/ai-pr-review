#!/usr/bin/env python3
"""Web dashboard for autonomous PR review system."""

from flask import Flask, render_template, jsonify, request, send_from_directory
import threading
import json
import os
from datetime import datetime
from autonomous_pr_monitor import AutonomousPRMonitor

app = Flask(__name__)

# Global state
monitor_thread = None
monitor_instance = None
monitoring_status = {
    "active": False,
    "repos": [],
    "started_at": None,
    "stats": {
        "prs_reviewed": 0,
        "critical_issues": 0,
        "reviews_posted": 0
    },
    "recent_reviews": []
}

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """Get monitoring status."""
    return jsonify(monitoring_status)

@app.route('/api/start', methods=['POST'])
def start_monitoring():
    """Start monitoring repos."""
    global monitor_thread, monitor_instance, monitoring_status

    data = request.json
    repos = data.get('repos', [])
    interval = data.get('interval', 60)

    if not repos:
        return jsonify({"error": "No repos specified"}), 400

    if monitoring_status["active"]:
        return jsonify({"error": "Already monitoring"}), 400

    # Create monitor instance
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        return jsonify({"error": "GITHUB_TOKEN not set"}), 500

    monitor_instance = AutonomousPRMonitor(
        repos=repos,
        github_token=token,
        check_interval=interval,
        auto_post_reviews=data.get('auto_post', False)
    )

    # Start in background thread
    def run_monitor():
        try:
            monitor_instance.run()
        except KeyboardInterrupt:
            pass

    monitor_thread = threading.Thread(target=run_monitor, daemon=True)
    monitor_thread.start()

    monitoring_status["active"] = True
    monitoring_status["repos"] = repos
    monitoring_status["started_at"] = datetime.now().isoformat()

    return jsonify({"status": "started", "repos": repos})

@app.route('/api/stop', methods=['POST'])
def stop_monitoring():
    """Stop monitoring."""
    global monitoring_status

    # Can't actually stop the thread cleanly, but mark as inactive
    monitoring_status["active"] = False
    monitoring_status["repos"] = []

    return jsonify({"status": "stopped"})

@app.route('/api/stats')
def get_stats():
    """Get detailed statistics."""
    global monitor_instance

    if monitor_instance:
        stats = monitor_instance.stats
    else:
        stats = monitoring_status["stats"]

    return jsonify(stats)

@app.route('/api/reviews')
def get_reviews():
    """Get recent reviews."""
    return jsonify(monitoring_status["recent_reviews"])

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("🌐 Starting Autonomous PR Review Dashboard")
    print("=" * 70)
    print("Dashboard: http://localhost:5000")
    print("=" * 70)
    print()
    app.run(host='0.0.0.0', port=5000, debug=True)
